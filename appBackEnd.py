'''
CS498 Group Project 
Gathering information from the Canvas API regarding the user who has the token
entered to the application

Robert Crispen
Wade Durham
Drew Willis
Spencer Gillaspie
'''

from canvasapi import Canvas
import os
from datetime import datetime
from datetime import date
from dateutil import tz
import collections
#TOKEN = '1139~bfXGBZAZHKoh7ZqH4GrUtoATy9M37hrTxhQNZ5JR4WR8Ycr6Zjm3vhU1VO7b5RT8'


class userCanvas:
    def __init__(self, TOKEN):
        URL = 'https://uk.instructure.com'
        if os.environ.get('Canvas_Key') is None:
            print('no key stored')
            #generate a key?
        if os.environ.get('Canvas_Token') is None:
            print('encrypted token not stored')
            #store encrypted token?
        self.canvas_api = Canvas(URL, TOKEN)
        self.user = self.canvas_api.get_current_user()
        self.courses = self.user.get_favorite_courses(enrollment_state = 'active')
        self.courseIds = []
        self.courseIdToCourseName = {}
        self.announcements = self.canvas_api.get_announcements(context_codes = [course for course in self.courses])
        self.todo = self.canvas_api.get_todo_items()
        
        # Get the course ids
        for course in self.courses:
            self.courseIds.append(str(course.id))
            
            self.courseIds.append(course.id)
            self.courseIdToCourseName[str(course.id)] = str(course.name)
            calendar = course.calendar
            
            self.assignments = course.get_assignments()

    # Returns an ordered dictionary of key=date, value=list of assignments due on
    #   that date, ordered by the keys
    def getAssignments(self):
        output = {}
        # Get the appropriate timezone objects
        utcTimeZone = tz.UTC
        localTimeZone = tz.tzlocal()
        
        for course in self.courses:
            assignments = course.get_assignments()
            for assignment in assignments:
                if hasattr(assignment, 'due_at_date'): #exclude assignments that dont have date associated
                    temp = str(assignment.due_at_date)
                    temp = temp[:10]
                    
                    date = datetime.strptime(temp, '%Y-%m-%d')
                    today = date.today()
                
                    if date >= today: #exclude assignments that have already occured
                         # Convert the datetime string in to a datetime object
                        canvasDateTimeObject = datetime.strptime(temp, '%Y-%m-%d')
                        
                        # Tell the object that it is in UTC time zone
                        canvasDateTimeObject = canvasDateTimeObject.replace(tzinfo=utcTimeZone)
                        
                        # Get a new datetime object in the local timezone
                        canvasDateTimeObjectLocal = canvasDateTimeObject.astimezone(localTimeZone)
                        
                        # Convert the local dattime object to a string output
                        canvasDueDateString = canvasDateTimeObjectLocal.strftime('%Y-%m-%d')
                        
                        if canvasDateTimeObjectLocal not in output.keys():
                            output[canvasDateTimeObjectLocal] = []
                        output[canvasDateTimeObjectLocal].append([str(assignment), str(course.id)])
                        
        o_assignments = collections.OrderedDict(sorted(output.items()))#ordered dictionary (by date) to avoid headaches
        assII = collections.OrderedDict([(k.strftime('%Y-%m-%d'), v) for k, v in o_assignments.items()])
        
        return assII
    
    # ex. announcement.title = Week 10 reminders
    # ex. announcement.context_code = course_2031359
    # Returns a dict of courseId, list of announcements for that course pairs
    def getAnnouncements(self):
        output = {}
        for announcement in self.announcements:
            courseCode = announcement.context_code[announcement.context_code.index('_') + 1:]
            if output.__contains__(courseCode):
                output[courseCode].append(announcement.title)
            else:
                output[courseCode] = [announcement.title]
        
        return output
    
    # Returns a dict of courseId, list of todos for that course pairs
    def getToDo(self):
        output = {}
        
        for task in self.todo:
            if output.__contains__(task.course_id):
                output[str(task.course_id)].append(task)
            else:
                output[str(task.course_id)] = [task]
                
        return output
    
    # Returns a list of dictionaries of class, grade pairs
    def getGrades(self):
        enrollments = self.user.get_enrollments()
        output = []
        for enrollment in enrollments:
            if enrollment.course_id in self.courseIds:
                output.append({ 'class': str(enrollment.course_id),
                               'grade': str(enrollment.grades['current_grade']) if hasattr(enrollment, 'grades') and 'current_grade' in enrollment.grades else ''
                    })
                
        return output
    
    # Returns a dict of course ids, color code paris
    def getColors(self):
        colors = self.user.get_colors()
        Colors = {courseID[7:]:color for (courseID, color) in colors['custom_colors'].items() if courseID[7:] in self.courseIds }
        
        return Colors
    
    
    def getCourseIdsToCourseName(self):
        return self.courseIdToCourseName
