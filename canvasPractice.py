'''
CS498 Group Project 
Gathering relevant information from the Canvas API with Token


'''
from canvasapi import Canvas
import os
import re
import cryptography 

TOKEN = '1139~bfXGBZAZHKoh7ZqH4GrUtoATy9M37hrTxhQNZ5JR4WR8Ycr6Zjm3vhU1VO7b5RT8'


class userCanvas:
    def __init__(self):
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
        self.announcements = self.canvas_api.get_announcements(context_codes = [course for course in self.courses])
        self.todo = self.canvas_api.get_todo_items()
        for course in self.courses:
            print(course)
            self.courseIds.append(str(course.id))
            print('Color in Canvas: '+str(course.course_color))
            self.courseIds.append(course.id)
            calendar = course.calendar
            print(calendar)
            self.assignments = course.get_assignments()
            for assignment in self.assignments:
                print('\t'+str(assignment)+' Due At: '+(str(assignment.due_at_date) if hasattr(assignment, 'due_at_date') else ''))
        print('-------------------------------')

        print('Notifications: ')

    def getAnnouncements(self):
        output = ""
        for announcement in self.announcements:
            output += str(announcement)+'\n'
            print('\t'+str(announcement))
        return output
    def getToDo(self):
        output = ""
        print('\nToDo: ')  
        for task in self.todo:
            output += str(task.assignment['name']) + '\n\t' +str(task.assignment['due_at'])
            print(task.assignment['name'])
            print('\t'+str(task.assignment['due_at']))
        return output
    def getGrades(self):
        
        print('Grade:')
        enrollments = self.user.get_enrollments()
        output = ""
        for enrollment in enrollments:
            if enrollment.course_id in self.courseIds:
                output += str(enrollment.course_id)+": "+str(enrollment.grades['current_grade']) if hasattr(enrollment, 'grades') and 'current_grade' in enrollment.grades else ''
                output += '\n'
                print(str(enrollment.course_id)+": "+str(enrollment.grades['current_grade']) if hasattr(enrollment, 'grades') and 'current_grade' in enrollment.grades else '')
        return output
    def getColors(self):
        colors = self.user.get_colors()
        Colors = {courseID[7:]:color for (courseID, color) in colors['custom_colors'].items() if courseID[7:] in self.courseIds }
        print(Colors)

'''
Playing with encryption of Token
'''

