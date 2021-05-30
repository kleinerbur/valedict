from course   import *
from pyfiglet import Figlet
from colr     import color
from shutil   import copyfile, move
import json
import sys, os
import winshell
import questionary

from pathlib import Path

SOURCE_DIR = os.path.dirname(os.path.abspath(__file__)) + "\\"
PARENT_DIR = SOURCE_DIR.removesuffix("src\\")
ASSETS_DIR = PARENT_DIR + "assets\\"

profile = winshell.folder("profile")
startmenu = profile + "\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\"
startup = startmenu + "Programs\\Startup\\"
pyw = sys.executable.replace("python.exe", "pythonw.exe")

pid = None

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

confirm_style = questionary.Style([
    ("qmark", "fg:black"),
    ("question", "fg:blue"),
    ("answer", "fg:white bold"),
    ("pointer", "fg:black"),
    ("highlighted", "fg:white bold"),
    ("selected", "fg:white bold"),
    ("instruction", "fg:white"),
    ("text", "fg:gray")
])

days       = ["[ MONDAY ]", "[ TUESDAY ]", "[ WEDNESDAY ]", "[ THURSDAY ]", "[ FRIDAY ]"]
days_lower = ["monday", "tuesday", "wednesday", "thursday", "friday"]
days_short = ["mon.", "tue.", "wed.", "thu.", "fri."]

clear = lambda: os.system('cls')

def hh_mm(time):
    h = time // 60
    m = time %  60
    return "{:02d}:{:02d}".format(h,m)

def print_logo(padding = 0):
    clear()
    print("\n" * padding)
    lines = Figlet(font="slant").renderText("valedict").split("\n")
    for line in lines:
        print(color("{:^100s}".format(line), fore="009050"))

def resize_window(width, height):
    os.system('mode con: cols={} lines={}'.format(width, height))

def save_data(courses):
    with open(PARENT_DIR + "valedict_data.json", "w", encoding='utf-8') as datafile:
        datafile.seek(0)
        json.dump(courses, datafile, default=lambda x: x.__dict__, indent=4, ensure_ascii=False, )
    courses.sort(key=lambda x: x.name)

def load_data(courses):
    with open(PARENT_DIR + "valedict_data.json", encoding='utf-8') as datafile:
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
            courses.sort(key=lambda x: x.name)
        except(json.JSONDecodeError):
            courses = []


def main_menu(pid):

    choices = []

    if pid is None:
        choices.append("{:^93s}".format("Start process"))
    else:
        choices.append("{:^93s}".format("Stop process"))

    choices += [
        "{:^93s}".format("List courses"),
        "{:^93s}".format("Print schedule"),
        "{:^93s}".format("Reload data"),
        "{:^93s}".format("Open JSON in notepad"),
    ]

    if (os.path.exists(startup + "\\valedict_process.lnk")):
        choices.append("{:^93s}".format("Remove from startup"))
    else:
        choices.append("{:^93s}".format("Run on system startup"))

    choices.append("{:^93s}".format("Exit"))

    choice = questionary.select(
        "{:^95s}".format("[ MENU ]"),
        style   = custom_style,
        choices = choices
    ).ask()

    return choice

def link_launcher(create_desktop_shortcut = False):
    with winshell.shortcut(PARENT_DIR + "Valedict") as link:
        link.path = SOURCE_DIR + "valedict_launcher.py"
        link.description = "Valedict Launcher"
        link.icon_location = (ASSETS_DIR + "valedict.ico", 0)
    
    if os.path.exists(SOURCE_DIR + "Valedict.lnk"):
        # link is created in src folder during installation
        # this is a workaround
        move(SOURCE_DIR + "Valedict.lnk",
             PARENT_DIR + "Valedict.lnk")

    copyfile(PARENT_DIR + "Valedict.lnk",
             startmenu  + "Valedict.lnk")    
    if (create_desktop_shortcut):
        copyfile(PARENT_DIR + "Valedict.lnk",
                 profile    + "\\Desktop\\Valedict.lnk") 

def link_process(enabled_on_startup = False):
    with winshell.shortcut(PARENT_DIR + "valedict_process") as link:
            link.path = pyw
            link.description = "valedict_process"
            link.arguments = PARENT_DIR + "valedict.py"
            link.icon_location = (ASSETS_DIR + "valedict.ico", 0)
    if os.path.exists(SOURCE_DIR + "valedict_process.lnk"):
        # link is created in src folder during installation
        # this is a workaround
        move(SOURCE_DIR + "valedict_process.lnk",
             PARENT_DIR + "valedict_process.lnk")
    if os.path.exists(profile + "\\Desktop\\valedict_process.lnk"):
        # for some reason, a shortcut is placed on the desktop
        # if the program was launched from a desktop shortcut;
        # I couldn't fix it so this is a workaround
        os.remove(profile + "\\Desktop\\valedict_process.lnk")
    if enabled_on_startup:
        copyfile(PARENT_DIR + "valedict_process.lnk",
                 startup    + "valedict_process.lnk")


if not os.path.exists(PARENT_DIR + "valedict_data.json"):
    open(PARENT_DIR + "valedict_data.json", "w")