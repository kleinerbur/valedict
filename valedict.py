from datetime          import datetime
from json.decoder      import JSONDecodeError
from notification      import NotificationSender
from course            import Course

import atexit
import json
import time
import os

SOURCE_DIR = os.path.dirname(os.path.abspath(__file__)) + "\\"

def exit_handler():
    vdict.save_data()
atexit.register(exit_handler)

def hh_mm(time):
    h = time // 60
    m = time %  60
    return "{:02d}:{:02d}".format(h,m)

class Valedict:
    def __init__(self):
        self.courses = []
        with open(SOURCE_DIR + "valedict_data.json") as datafile:
            try:
                data = json.load(datafile)
                for x in data:
                    c = Course("tempname", "tempcode")
                    c.__dict__ = json.loads(json.dumps(x))
                    if hasattr(c, "seminar"):
                        c.set_seminar(c.seminar["day"], hh_mm(c.seminar["start_time"]))
                    if hasattr(c, "lecture"):
                        c.set_lecture(c.lecture["day"], hh_mm(c.lecture["start_time"]))
                    self.courses.append(c)
            except(JSONDecodeError):
                self.courses = []
            self.sender = NotificationSender()

    def save_data(self):
        with open(SOURCE_DIR + "valedict_data.json", "w") as datafile:
            datafile.seek(0)
            print(json.dumps(self.courses, default=lambda x: x.__dict__, indent=4), file=datafile)

    def tick(self):
        h = int(datetime.now().hour)
        m = int(datetime.now().minute)
        time = h * 60 + m
        for course in self.courses:
            if hasattr(course, "lecture"):
                if course.lecture.check_time(time):
                    self.sender.send(course.name, hh_mm(course.lecture.start_time))
            if hasattr(course, "seminar"):
                if course.seminar.check_time(time):
                    self.sender.send(course.name, hh_mm(course.seminar.start_time))
        self.save_data()

# MAIN

vdict = Valedict()
# c = Course("Adatbazisok I", "IP-18bAB1")
# c.set_lecture(1, "08:30")
# c.set_seminar(1, "12:15")
# vdict.courses.append(c)
# c = Course("Numerikus modszerek I", "IP-18bNM1")
# c.set_lecture(2, "10:15")
# c.set_seminar(3, "08:30")
# vdict.courses.append(c)
# c = Course("Tobbvaltozos fuggvenytan", "IP-18aTVFT")
# c.set_lecture(3, "14:15")
# c.set_seminar(4, "10:00")
# vdict.courses.append(c)
vdict.sender.send("Adatbázisok I", "8:30")