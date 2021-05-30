from datetime      import datetime
from notification  import NotificationSender
from tools         import *

import atexit
import json
import time


def exit_handler():
    # vdict.save_data()
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
        save_data(self.courses)

    def tick(self):
        load_data(self.courses)
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

# MAIN

vdict = Valedict()
vdict.sender.welcome()
while True:
    vdict.tick()
    time.sleep(60)