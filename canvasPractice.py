from canvasapi import Canvas
import re

TOKEN = '1139~bfXGBZAZHKoh7ZqH4GrUtoATy9M37hrTxhQNZ5JR4WR8Ycr6Zjm3vhU1VO7b5RT8'

URL = 'https://uk.instructure.com'

canvas_api = Canvas(URL, TOKEN)

user = canvas_api.get_current_user()

courses = user.get_favorite_courses(enrollment_state = 'active')
courseIds = []
for course in courses:
    print(course)
    courseIds.append(course.id)
    calendar = course.calendar
    print(calendar)
    assignments = course.get_assignments()
    for assignment in assignments:
        print('\t'+str(assignment)+' Due At: '+(str(assignment.due_at_date) if hasattr(assignment, 'due_at_date') else ''))
    print('-------------------------------')

print('Notifications: ')

for event in calendar:
    print(type(event))
    
announcements = canvas_api.get_announcements(context_codes = [course for course in courses])

for announcement in announcements:
    print('\t'+str(announcement))
print('\nToDo: ')  
todo = canvas_api.get_todo_items()
for task in todo:
    print(task.assignment['name'])
    print('\t'+str(task.assignment['due_at']))
print('Grade:')
enrollments = user.get_enrollments()
for enrollment in enrollments:
    if enrollment.course_id in courseIds:
        print(str(enrollment.course_id)+": "+str(enrollment.grades['current_grade']) if hasattr(enrollment, 'grades') and 'current_grade' in enrollment.grades else '')