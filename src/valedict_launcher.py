from tools  import *

import winsound
import atexit
import questionary
import winshell
import time
import webbrowser
import subprocess
import signal

os.system("title valedict")
os.system('mode con: cols=100 lines=25')

def exit_handler():
    clear()
    winsound.PlaySound(ASSETS_DIR + "valedict_exit.wav", winsound.SND_FILENAME)

atexit.register(exit_handler)



# MAIN

winsound.PlaySound(ASSETS_DIR + "valedict_chime.wav", winsound.SND_ASYNC)

courses = []
load_data(courses)

while(True):

    resize_window(100, 25)
    clear() # for vscode terminal
    
    print_logo()

    try:
        with open(".pid") as file:
            pid = int(file.readline().strip())
    except FileNotFoundError:
        pid = None
    except EOFError:
        pid = None

    choice = main_menu(pid)

    try:
        choice = choice.strip()
    except:
        exit()


    if choice == "Start process":
        with open(".pid", "w") as file:
            process = subprocess.Popen("{} \"{}\"".format(pyw, SOURCE_DIR + "valedict.py"),
                             start_new_session=True)
            pid = process.pid
            print(pid, file=file)        


    elif choice == "Stop process":
        os.remove(".pid")
        try:
            os.kill(pid, signal.SIGBREAK)
        except:
            continue


    elif choice == "List courses":
        while True:
            courseNames = []
            for course in courses:
                courseNames.append(" {:<15} | {}".format(course.code, course.name))

            resize_window(100, len(courseNames)*2 + 10)
            print_logo()

            courseName = questionary.select(
                "{:^95s}".format("[ COURSES ]"),
                style   = custom_style,
                choices = [ "{:^93s}".format("[ Add course ]"), ]
                        + courseNames
                        + ["{:^93s}".format("[ Go back ]")]
            ).ask()

            if courseName is None or courseName.strip() == "[ Go back ]": break
            elif courseName.strip() == "[ Add course ]":
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
                        with open(PARENT_DIR + "valedict_data.json", "w") as datafile:
                            datafile.seek(0)
                            print(json.dumps(courses, default=lambda x: x.__dict__, indent=4), file=datafile)
                        print(color("Added course {} - {}.".format(code, name), fore="green"))
                    else:
                        print("Aborting...")
                time.sleep(1)
            else:
                while True:
                    print_logo()

                    course = [x for x in courses if x.code == courseName.split("|")[0].strip()][0]
                    choices = []

                    if hasattr(course, "lecture"):
                        listitem = "LECTURE: {} {}".format(days_short[course.lecture.day - 1], hh_mm(course.lecture.start_time))
                    else:
                        listitem = "LECTURE: {} {}".format("-", "-")
                    choices.append("{:^93s}".format(listitem))
                    
                    if hasattr(course, "seminar"):
                        listitem = "SEMINAR: {} {}".format(days_short[course.seminar.day - 1], hh_mm(course.seminar.start_time))
                    else:
                        listitem = "SEMINAR: {} {}".format("-", "-")
                    choices.append("{:^93s}".format(listitem))

                    choices.append("{:^93s}".format("[ Go back ]"))

                    choice = questionary.select(
                        "{:^95s}\n".format(courseName.strip()),
                        style = custom_style,
                        choices = choices
                    ).ask()
                
                    if choice is None or choice.strip() == "[ Go back ]": break

                    print()
                    new_day = questionary.select(
                        "{:^95s}".format("Set day for class:"),
                        style   = custom_style,
                        choices = ["{:^93s}".format(day) for day in days_lower]
                                + ["", "{:^93s}".format("[ Go back ]")]
                    ).ask()

                    if new_day is None or len(new_day) == 0 or new_day.strip() == "[ Go back ]": continue

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
                        courses[courses.index(course)].set_lecture(days_lower.index(new_day.strip()) + 1, new_time)                
                        with open(PARENT_DIR + "valedict_data.json", "w") as datafile:
                            datafile.seek(0)
                            print(json.dumps(courses, default=lambda x: x.__dict__, indent=4), file=datafile)
                    elif confirmed and class_type == "seminar":
                        courses[courses.index(course)].set_seminar(days_lower.index(new_day.strip()) + 1, new_time)
                        with open(PARENT_DIR + "valedict_data.json", "w") as datafile:
                            datafile.seek(0)
                            print(json.dumps(courses, default=lambda x: x.__dict__, indent=4), file=datafile)
                    else:
                        print("Aborting...")


    elif choice == "Print schedule":
        
        lectures = [(course.name + " [L]", course.lecture.day, course.lecture.start_time) for course in courses if hasattr(course, "lecture")]
        seminars = [(course.name + " [S]", course.seminar.day, course.seminar.start_time) for course in courses if hasattr(course, "seminar")]
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


    elif choice == "Reload data":
        clear()
        load_data(courses)


    elif choice == "Open JSON in notepad":
        clear()
        webbrowser.open(PARENT_DIR + "valedict_data.json")


    elif choice == "Run on system startup":
        clear()
        link_process()


    elif choice == "Remove from startup":
        clear()
        os.remove(startup+"valedict_process.lnk")


    elif choice == "Exit":
        exit()
