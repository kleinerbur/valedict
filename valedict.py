from datetime          import datetime
from notification      import NotificationSender

import atexit
import json
import time

from tools import *

def exit_handler():
    vdict.save_data()
    vdict.sender.goodbye()

atexit.register(exit_handler)

def hh_mm(time):
    h = time // 60
    m = time %  60
    return "{:02d}:{:02d}".format(h,m)

class Valedict:
    def __init__(self):
        self.courses = []
        load_data(self.courses)
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
vdict.sender.welcome()
while True:
    vdict.tick()
    time.sleep(60)