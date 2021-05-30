import json, re
from datetime import datetime

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

        if not re.match("((0?[0-9])|(1[0-9])|(2[0-3])):[0-5][0-9]", start_time):
            raise ValueError("Start time was not in correct format (hh:mm).")
        
        self.type = type
        self.day  = day
        h = int(start_time.split(":")[0])
        m = int(start_time.split(":")[1])
        self.start_time = h * 60 + m
    
    def check_time(self, time):
        return datetime.today().weekday() + 1 == self.day and self.start_time - 10 == time
