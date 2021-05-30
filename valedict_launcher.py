from pyfiglet import Figlet
from colr     import color
from json     import JSONDecodeError
from course   import Course, Class
from shutil   import copyfile
import winsound
import atexit
import questionary
import os
import sys
import json
import winshell
import time
import webbrowser
import re

os.system("title valedict")
os.system('mode con: cols=100 lines=25')

clear = lambda: os.system('cls')
profile = winshell.folder("profile")
startup = profile + "\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup"
SOURCE_DIR = os.path.dirname(os.path.abspath(__file__))

def hh_mm(time):
    h = time // 60
    m = time %  60
    return "{:02d}:{:02d}".format(h,m)

def print_logo():
    clear()
    lines = Figlet(font="slant").renderText("valedict").split("\n")
    for line in lines:
        print(color("{:^100s}".format(line), fore="009050"))

def load_data(courses):
    with open(SOURCE_DIR + "\\valedict_data.json") as datafile:
        try:
            data = json.load(datafile)
            for x in data:
                c = Course("tempname", "tempcode")
                c.__dict__ = json.loads(json.dumps(x))
                if hasattr(c, "seminar"):
                    c.set_seminar(c.seminar["day"], hh_mm(c.seminar["start_time"]))
                if hasattr(c, "lecture"):
                    c.set_lecture(c.lecture["day"], hh_mm(c.lecture["start_time"]))
                courses.append(c)
        except(JSONDecodeError):
            courses = []

def exit_handler():
    clear()
    winsound.PlaySound(SOURCE_DIR + "\\valedict_exit.wav", winsound.SND_FILENAME)

winsound.PlaySound(SOURCE_DIR + "\\valedict_chime.wav", winsound.SND_ASYNC)
atexit.register(exit_handler)

custom_style = questionary.Style([
    ("qmark", "fg:black"),
    ("question", "fg:blue"),
    ("answer", "fg:white bold"),
    ("pointer", "fg:black"),
    ("highlighted", "fg:white bold"),
    ("selected", "fg:white bold"),
    ("instruction", "fg:black"),
    ("text", "fg:gray")
])


# MAIN


courses = []
load_data(courses)


days = ["[ MONDAY ]", "[ TUESDAY ]", "[ WEDNESDAY ]", "[ THURSDAY ]", "[ FRIDAY ]"]
days_lower = ["monday", "tuesday", "wednesday", "thursday", "friday"]
days_short = ["mon.", "tue.", "wed.", "thu.", "fri."]

while(True):

    os.system('mode con: cols=100 lines=25')
    clear() # for vscode terminal
    
    print_logo()

    if (os.path.exists(startup + "\\valedict.lnk")):
        choice = questionary.select(
            "{:^95s}".format("[ MENU ]"),
            style   = custom_style,
            choices = [
                "{:^93s}".format("List courses"),
                "{:^93s}".format("Print schedule"),
                "{:^93s}".format("Add course"),
                "{:^93s}".format("Reload data"),
                "{:^93s}".format("Open JSON in notepad"),
                "{:^93s}".format("Remove from startup"),
                "{:^93s}".format("Exit")
            ]
        ).ask().strip()
    else:
        choice = questionary.select(
            "{:^95s}".format("[ MENU ]"),
            style   = custom_style,
            choices = [
                "{:^93s}".format("List courses"),
                "{:^93s}".format("Print schedule"),
                "{:^93s}".format("Add course"),
                "{:^93s}".format("Reload data"),
                "{:^93s}".format("Open JSON in notepad"),
                "{:^93s}".format("Run on system startup"),
                "{:^93s}".format("Exit")
            ]
        ).ask().strip()

    if choice == "List courses":
        while True:
            courseNames = []
            for course in courses:
                courseNames.append(" {} | {}".format(course.code, course.name))

            os.system('mode con: cols=100 lines={}'.format((len(courseNames)+5)*2))
            print_logo()

            courseName = questionary.select(
                "{:^95s}".format("[ COURSES ]"),
                style   = custom_style,
                choices = courseNames + ["{:^93s}".format("[ Go back ]")]
            ).ask()

            if courseName is None or courseName == "[ Go back ]": break
            
            print_logo()

            course = [x for x in courses if x.code == courseName.split("|")[0].strip()][0]
            choices = []
            if hasattr(course, "lecture"): choices.append("LECTURE: {} {}".format(days_short[course.lecture.day - 1], hh_mm(course.lecture.start_time)))
            else:                          choices.append("LECTURE: {} {}".format("-", "-"))
            if hasattr(course, "seminar"): choices.append("SEMINAR: {} {}".format(days_short[course.seminar.day - 1], hh_mm(course.seminar.start_time)))
            else:                          choices.append("SEMINAR: {} {}".format("-", "-"))
            choice = questionary.select(
                "{:^95s}".format(courseName.strip()),
                style = custom_style,
                choices = choices
            ).ask()
        
            if choice is None: continue

            new_day = questionary.select(
                "Day:",
                style   = custom_style,
                choices = days_lower
            ).ask()

            if new_day is None: continue

            new_time = questionary.text(
                "Time (hh:mm):",
                style = custom_style,
                validate = lambda x: len(x) > 0
            ).ask()
            if new_time is None: continue

            while not re.match("((0?[0-9])|(1[0-9])|(2[0-3])):[0-5][0-9]", new_time) and not new_time is None:
                print(color("Incorrect format.", fore="red"))
                new_time = questionary.text(
                    "Time (hh:mm):",
                    style = custom_style,
                    validate = lambda x: len(x) > 0
                ).ask()
            if new_time is None: continue

            class_type = choice.strip().lower()[0:7]
            confirmed = questionary.confirm(
                "Add {} at {} on {} for {}?".format(class_type, new_time, new_day, courseName.split("|")[1].strip()),
                default = True,
                style   = custom_style,
                auto_enter = False
            ).ask()

            if confirmed and class_type == "lecture":
                courses[courses.index(course)].set_lecture(days_lower.index(new_day) + 1, new_time)                
                with open(SOURCE_DIR + "\\valedict_data.json", "w") as datafile:
                    datafile.seek(0)
                    print(json.dumps(courses, default=lambda x: x.__dict__, indent=4), file=datafile)
            elif confirmed and class_type == "seminar":
                courses[courses.index(course)].set_seminar(days_lower.index(new_day) + 1, new_time)
                with open(SOURCE_DIR + "\\valedict_data.json", "w") as datafile:
                    datafile.seek(0)
                    print(json.dumps(courses, default=lambda x: x.__dict__, indent=4), file=datafile)
            else:
                print("Aborting...")


    if choice == "Print schedule":
        
        lectures = [(course.name, course.lecture.day, course.lecture.start_time) for course in courses if hasattr(course, "lecture")]
        seminars = [(course.name, course.seminar.day, course.seminar.start_time) for course in courses if hasattr(course, "seminar")]
        classes = (lectures + seminars)
        classes = sorted(classes, key=lambda x:x[2])
        schedule = [""]
        for i in range(1, 6):
            schedule.append("{:^93s}".format(days[i-1]))
            for name, day, start_time in filter(lambda x: x[1] == i, classes):
                schedule.append("{:>35s}   {}".format(hh_mm(start_time), name))
            schedule.append("")

        os.system('mode con: cols=100 lines={}'.format(len(schedule)*2))
        print_logo()
        questionary.select(
            "{:^95s}".format("[ SCHEDULE ]"),
            style   = custom_style,
            choices = schedule
        ).ask()        



    elif choice == "Add course":
        print_logo()
        name = questionary.text(
            "Course name:",
            validate = lambda name: len(name) > 0,
            style = custom_style
        ).ask()
        if name is None: continue
        code = questionary.text(
            "Course code:",
            validate = lambda name: len(name) > 0,
            style = custom_style
        ).ask()
        if code is None: continue
        if code in [course.code for course in courses]:
            print("There is already a course in the database with the same code.")
        else:
            confirmed = questionary.confirm(
                "Add course {} - {}?".format(code, name),
                default = True,
                style   = custom_style,
                auto_enter = False
            ).ask()
            if confirmed:
                courses.append(Course(name, code))
                with open(SOURCE_DIR + "\\valedict_data.json", "w") as datafile:
                    datafile.seek(0)
                    print(json.dumps(courses, default=lambda x: x.__dict__, indent=4), file=datafile)
                print(color("Added course {} - {}.".format(code, name), fore="green"))
            else:
                print("Aborting...")
        time.sleep(1)


    elif choice == "Reload data":
        clear()
        load_data(courses)


    elif choice == "Open JSON in notepad":
        clear()
        webbrowser.open(SOURCE_DIR + "\\valedict_data.json")


    elif choice == "Run on system startup":
        clear()
        pyw = sys.executable.replace("python.exe", "pythonw.exe")
        with winshell.shortcut("valedict") as link:
            link.path = pyw
            link.description = "Valedict"
            link.arguments = SOURCE_DIR + "\\valedict.py"           
        copyfile(SOURCE_DIR+"\\valedict.lnk", startup+"\\valedict.lnk")


    elif choice == "Remove from startup":
        clear()
        os.remove(startup+"\\valedict.lnk")


    elif choice == "Exit" or choice is None:
        clear()
        exit()
