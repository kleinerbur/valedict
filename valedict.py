from datetime import datetime
from notification import NotificationSender
import re, json, sys

class CourseEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__


class Course:
    def __init__(self, name, code):
        # validating args
        if not (isinstance(name, str) and isinstance(name, str)):
            raise ValueError("Course name and code should be strings.")

        self.name = name
        self.code = code
    
    def __str__(self):
        return CourseEncoder().encode(self)

    def set_seminar(self, day, start_time):
        self.seminar = Class("seminar", day, start_time)
    
    def set_lecture(self, day, start_time):
        self.lecture = Class("lecture", day, start_time)


class Class:
    def __init__(self, type, day, start_time):
        # validating args
        if type not in ["seminar", "lecture"]:
            raise ValueError("Failed to parse type of class; should be \"seminar\" or \"lecture\".")

        if day not in range(1, 8):
            raise ValueError("Failed to parse day of the week; should be an integer between 1 and 7.")

        if not re.match("((1?[0-9])|(2[0-3])):[0-5][0-9]", start_time):
            raise ValueError("Start time was not in correct format (hh:mm).")
        
        self.type = type
        self.day  = day
        h = int(start_time.split(":")[0])
        m = int(start_time.split(":")[1])
        self.start_time = h * 60 + m
    
    def check_time(self, time):
        print(datetime.today().weekday() + 1, self.day)
        print(time, self.start_time - 10)
        return datetime.today().weekday() + 1 == self.day and self.start_time - 10 == time


class Valedict:
    def __init__(self):
        self.courses = []
        with open("valedict_data.json") as datafile:
            data = json.load(datafile)
            for x in data:
                c = Course("tempname", "tempcode")
                c.__dict__ = json.loads(json.dumps(x))
                if hasattr(c, "seminar"):
                    h = c.seminar["start_time"] // 60
                    m = c.seminar["start_time"] % 60
                    c.set_seminar(c.seminar["day"], "{:02d}:{:02d}".format(h,m,"02"))
                if hasattr(c, "lecture"):
                    h = c.lecture["start_time"] // 60
                    m = c.lecture["start_time"] % 60
                    c.set_lecture(c.lecture["day"], "{:02d}:{:02d}".format(h,m,"02"))
                self.courses.append(c)
            self.sender = NotificationSender()

    def save_data(self):
        with open("valedict_data.json", "w") as datafile:
            datafile.seek(0)
            print(json.dumps(self.courses, default=lambda x: x.__dict__, indent=4), file=datafile)

    def tick(self):
        h = int(datetime.now().hour)
        m = int(datetime.now().minute)
        time = h * 60 + m
        for course in self.courses:
            if hasattr(course, "lecture"):
                if course.lecture.check_time(time):
                    h = course.lecture.start_time // 60
                    m = course.lecture.start_time % 60
                    self.sender.send(course.name, "{:02d}:{:02d}".format(h,m))
            if hasattr(course, "seminar"):
                if course.seminar.check_time(time):
                    h = course.seminar.start_time // 60
                    m = course.seminar.start_time % 60
                    self.sender.send(course.name, "{:02d}:{:02d}".format(h,m))
        self.save_data()


vdict = Valedict()
vdict.tick()