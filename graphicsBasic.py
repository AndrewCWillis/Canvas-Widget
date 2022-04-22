# -*- coding: utf-8 -*-
'''
CS498 Group Project 
A Foundation for the Graphics
'''
import enum
from itertools import count
from operator import countOf
from textwrap import fill
from turtle import bgcolor, width
from winreg import HKEY_CLASSES_ROOT, HKEY_CURRENT_USER
import canvasPractice
import tkinter as tk
from tkinter import BOTH, E, LEFT, NE, NS, NW, RIGHT, TOP, VERTICAL, W, Y, Button, PhotoImage, Toplevel, ttk
import os
from canvasapi import Canvas
from datetime import datetime
from datetime import timedelta
from dateutil import tz
from datetime import date
from PIL import Image
from PIL import ImageTk as itk

class widget:
    def __init__(self):
        try:
            settingsfile = open("settings.txt", 'r')
            self.staylogged = int(settingsfile.readline())
            self.darkmode = str(settingsfile.readline())
            settingsfile.close()
            self.darkmode = self.darkmode.strip()
        except:
            settingsfile = open("settings.txt", 'w')
            self.staylogged = 0
            self.darkmode = "light"
            settingsfile.write(str(self.staylogged))
            settingsfile.write(self.darkmode)
            settingsfile.close()

        self.URL = 'https://uk.instructure.com'
        file = open('canvas_api_token.txt', 'r')
        TOKEN = file.readline()
        file.close()
        self.stuCanvas = canvasPractice.userCanvas(TOKEN)
        #self.stuCanvas.getAssignments()
        self.root = tk.Tk()
        #root.tk.call('lappend', 'auto_path', 'Azure-ttk-theme-main/azure dark')
        #root.tk.call('package', 'require', 'azure dark')
        self.root.tk.call('source', 'Azure-ttk-theme-main/Azure-ttk-theme-main/azure.tcl')
        self.root.tk.call('set_theme', self.darkmode)
        self.style = ttk.Style()
        #self.style.theme_use('dark')
        #root.tk.call('lappend', 'auto_path', 'awthemes-10.4.0')
        #root.tk.call('package', 'require', 'awdark')

        self.gearIcon, self.refreshIcon = self.getIcons()

        self.root.title("Canvas Widget")
        self.root.geometry('500x500')
        self.tabControl = ttk.Notebook(self.root)

        # Control frame to hold the buttons horizontally
        self.top = tk.Frame(self.root)
        self.top.pack(side=TOP, anchor=NE)

        #setting button adding to the top right
        self.token = TOKEN
        self.settingsButton = tk.Button(text = "Settings", image=self.gearIcon, command=self.open_popup)
        self.stayLoggedIn(self.staylogged)

        # Refresh Button, adjacent to settings button
        self.refreshButton = tk.Button(text = "Refresh", image=self.refreshIcon, command=self.open_popup)

        # Add the buttons to the control frame
        self.settingsButton.pack(in_=self.top, side=RIGHT)
        self.refreshButton.pack(in_=self.top, side=RIGHT)

        #setting up tabs 
        self.tab1 = ttk.Frame(self.tabControl)
        self.tab2 = ttk.Frame(self.tabControl)
        self.tab3 = ttk.Frame(self.tabControl)
        self.tab4 = ttk.Frame(self.tabControl)

        self.tabControl.add(self.tab1, text ='Grades')
        self.tabControl.add(self.tab2, text ='Announcements')
        self.tabControl.add(self.tab3, text ='Assignments')
        self.tabControl.add(self.tab4, text ='To Do')
        
        # Scrollbars for the below canvas'. The scrollbars are placed in the
        #   tab frames.
        self.sb1 = ttk.Scrollbar(self.tab1, orient=VERTICAL)
        self.sb2 = ttk.Scrollbar(self.tab2, orient=VERTICAL)
        self.sb3 = ttk.Scrollbar(self.tab3, orient=VERTICAL)
        self.sb4 = ttk.Scrollbar(self.tab4, orient=VERTICAL)
        
        # Canvas to go in the tab frames. This is so that the content can be
        #   made scrollable
        self.canvas1 = tk.Canvas(self.tab1, yscrollcommand=self.sb1.set)
        self.canvas2 = tk.Canvas(self.tab2, yscrollcommand=self.sb2.set)
        self.canvas3 = tk.Canvas(self.tab3, yscrollcommand=self.sb3.set)
        self.canvas4 = tk.Canvas(self.tab4, yscrollcommand=self.sb4.set)
        
        # Frames to put the actual content in. This frame will go inside the
        #   appropriate canvas and the canvas will go in the outer, tab frame.
        # We put the content in an inner frame since canvas' have strange ways
        #   of placing objects in them and making them scrollable. Having an inner
        #   frame with all the content makes this simpler.
        self.innerFrame1 = tk.Frame(self.canvas1)
        self.innerFrame2 = ttk.Frame(self.canvas2)
        self.innerFrame3 = ttk.Frame(self.canvas3)
        self.innerFrame4 = ttk.Frame(self.canvas4)
        
        # Whenever something is added to the innerFrame, 
        #   set all the inner frame to be scrollable and make the canvas as wide as the innerFrame
        self.innerFrame1.bind('<Configure>', 
                              func=lambda x: self.updateFrame(self.canvas1, self.innerFrame1))
        self.innerFrame2.bind('<Configure>', 
                              func=lambda x: self.updateFrame(self.canvas2, self.innerFrame2))
        self.innerFrame3.bind('<Configure>', 
                              func=lambda x: self.updateFrame(self.canvas3, self.innerFrame3))
        self.innerFrame4.bind('<Configure>', 
                              func=lambda x: self.updateFrame(self.canvas4, self.innerFrame4))

        # Tell the scrollbars the function to execute when they are changed
        self.sb1.config(command=self.canvas1.yview)
        self.sb2.config(command=self.canvas2.yview)
        self.sb3.config(command=self.canvas3.yview)
        self.sb4.config(command=self.canvas4.yview)
        
        self.tabControl.pack(expand = 1, fill ="both")

        self.displayGrades()
        self.displayAnnouncements()
        self.displayCalendar()

        self.displayTodos()
        
        self.root.iconbitmap('canvas_icon.ico')
        self.root.mainloop()

    # Update the root frame size to accomodate arbitrary width items and 
    #   let the canvas know that the scrollable area is the entire canvas.
    def updateFrame(self, canvas, innerFrame):
        # Set all the inner frame to be scrollable and make the canvas as wide as the innerFrame
        canvas.configure(scrollregion=canvas.bbox("all"), width=innerFrame.winfo_width())
        
        # Update the root window to be wide enough to fit the contents
        if self.root.winfo_width() < innerFrame.winfo_width():
            self.root.geometry(f'{innerFrame.winfo_width() + 50}x{self.root.winfo_height()}')    
            
            
    # Put the grades onto the grades tab
    def displayGrades(self):
        gradesList = self.stuCanvas.getGrades()
        idToName = self.stuCanvas.getCourseIdsToCourseName()
        Colors = self.stuCanvas.getColors()
    
        # For each class with a grade, add the class name and grade to the inner frame
        for i in range(len(gradesList)):
            ttk.Label(self.innerFrame1, 
                      text = '{}: {}'.format(idToName[gradesList[i]['class']], gradesList[i]['grade']),
                      justify = 'left',
                      background = Colors[gradesList[i]['class']],
                      borderwidth = 5,
                      relief = 'raised').grid(column = 0, 
                               row = i,
                               padx = 10,
                               pady = 10,
                               sticky = W)
        
        self.canvas1.create_window(0, 0, window=self.innerFrame1, anchor=NW) # Put the innerFrame in the canvas
        self.canvas1.pack(side=LEFT, anchor=NW, fill=BOTH) # Put the canvas in the tab frame
        self.sb1.pack(side=RIGHT, fill=Y) # Put the scrollbar in the tab frame
        
          
    def displayAnnouncements(self):
        announcementsDict = self.stuCanvas.getAnnouncements()
        idToName = self.stuCanvas.getCourseIdsToCourseName()
        Colors = self.stuCanvas.getColors()
        countOfRows = 0 # Counter for which row to place the next item
    
        # For every course there is an announcement for
        for courseKey in announcementsDict:
        # Put the class name as a 'header' of sorts
            ttk.Label(self.innerFrame2, 
                      text = str(idToName[courseKey]),
                      justify = 'left',
                      background = Colors[courseKey],
                      borderwidth = 5,
                      relief = 'raised').grid(column = 0, 
                               row = countOfRows,
                               padx = 10,
                               pady = 10,
                               sticky = W)
                      
        
            # For all the announcements for this course
            for announcement in announcementsDict[courseKey]:
            # Put the announcement under the 'header'
                ttk.Label(self.innerFrame2, 
                          text = str(announcement),
                          justify = 'left',
                          background = 'white',
                          borderwidth = 5).grid(column = 0, 
                                    row = countOfRows+1,
                                    padx = 50,
                                    pady = 10,
                                    sticky = W)
        
                countOfRows += 1
            countOfRows +=1
            
        
        self.canvas2.create_window(0, 0, window=self.innerFrame2, anchor=NW) # Put the innerFrame in the canvas
        self.canvas2.pack(side=LEFT, anchor=NW, fill=BOTH) # Put the canvas in the tab frame
        self.sb2.pack(side=RIGHT, fill=Y) # Put the scrollbar in the tab frame
        
    def displayTodos(self):
        todoDict = self.stuCanvas.getToDo()
        idToName = self.stuCanvas.getCourseIdsToCourseName()
        Colors = self.stuCanvas.getColors()
        countOfRows = 0 # Counter for which row to place the next item
    
        # Get the appropriate timezone objects
        utcTimeZone = tz.UTC
        localTimeZone = tz.tzlocal()
        
        # For every course there is an announcement for
        for courseKey in todoDict:
            # Put the class name as a 'header' of sorts
            ttk.Label(self.innerFrame4, 
                      text = str(idToName[courseKey]),
                      justify = 'left',
                      background = Colors[courseKey],
                      borderwidth = 5,
                      relief = 'raised').grid(column = 0, 
                               row = countOfRows,
                               padx = 10,
                               pady = 10,
                               sticky = W)
                      
        
            # For all the todo items for this course
            for todoItem in todoDict[courseKey]:
                # Find the object that this todo is about
                objectInTodo = {}
                objectInTodoAttr = ''
                for attr, value in todoItem.__dict__.items():
                    if attr == 'assignment' or attr == 'quiz':
                        objectInTodoAttr = attr
                        objectInTodo = value
                        # print(f'attr: {attr}, val: {value}')
                        
                # Convert the datetime string in the objectInTodo to a datetime object
                canvasDateTimeObject = datetime.strptime(objectInTodo["due_at"], '%Y-%m-%dT%H:%M:%SZ')
                
                # Tell the object that it is in UTC time zone
                canvasDateTimeObject = canvasDateTimeObject.replace(tzinfo=utcTimeZone)
                
                # Get a new datetime object in the local timezone
                canvasDateTimeObjectLocal = canvasDateTimeObject.astimezone(localTimeZone)
                
                # Conver the local dattime object to a string output
                canvasDueDateString = canvasDateTimeObjectLocal.strftime('%A, %B %d, %Y at %I:%M %p')
                
                todoString = f'Type: {todoItem.type.capitalize()}:\n{objectInTodoAttr.capitalize()}: {objectInTodo["name"]}\nDue at: {canvasDueDateString}'
                # Put the announcement under the 'header'
                ttk.Label(self.innerFrame4, 
                          text = todoString,
                          justify = 'left',
                          background = 'white',
                          borderwidth = 5).grid(column = 0, 
                                    row = countOfRows+1,
                                    padx = 50,
                                    pady = 10,
                                    sticky = W)
        
                countOfRows += 1
            countOfRows +=1
            
        self.canvas4.create_window(0, 0, window=self.innerFrame4, anchor=NW) # Put the innerFrame in the canvas
        self.canvas4.pack(side=LEFT, anchor=NW, fill=BOTH) # Put the canvas in the tab frame
        self.sb4.pack(side=RIGHT, fill=Y) # Put the scrollbar in the tab frame
        
    def displayCalendar(self):
        assignments = self.stuCanvas.getAssignments() #returns ordered dictionary sorted by datetime due date keys
        idToName = self.stuCanvas.getCourseIdsToCourseName()
        Colors = self.stuCanvas.getColors()
        numDays = 7
        today = date.today()
        #print(assignments)
        dayCells = [tk.Frame(self.innerFrame3, bg = 'light gray', width = 200, height = 200) for day in range(numDays)]
        for i in range(numDays):
            day = today + timedelta(days=i)
            ttk.Label(dayCells[i], 
                      text = day.strftime('%A, %m/%d/%y'), justify = 'center', font = 'bold', background = 'gray',
                                               borderwidth = 5).grid(row = 0, column = 0, sticky = W, padx = 2)
            key = day.strftime('%Y-%m-%d')
            if key in assignments.keys():
                for j in range(len(assignments[key])):#multiple assignments due the same day
            
                    ttk.Label(dayCells[i], 
                      text = assignments[key][j],font = 'bold', justify = 'center', background = 'light gray',
                                                borderwidth = 5, wraplengt=140).grid(row = 1 + j, column = 0, sticky = W, padx = 2)
            else:
                ttk.Label(dayCells[i], 
                      text = 'Nothing to Do :)', font = 'bold',justify = 'center', background = 'light gray',
                                       borderwidth = 5, wraplengt=140).grid(row = 1, column = 0, sticky = W, padx = 2)
        r = 0 
        for i, day in enumerate(dayCells):
            if (i % 7 == 0 and i != 0) or r == 6:
                r += 1
                
            day.grid(row = r, column = 7 - (i%7), sticky = W, padx = 2)
 
        self.canvas3.create_window(0, 0, window=self.innerFrame3, anchor=NW) # Put the innerFrame in the canvas
        self.canvas3.pack(side=LEFT, anchor=NW, fill=BOTH) # Put the canvas in the tab frame
        self.sb3.pack(side=RIGHT, fill=Y) # Put the scrollbar in the tab frame

    def stayLoggedIn(self, SLI):
        file = os.path.exists("canvas_api_token.txt")
        if(SLI == 1):
            if not file:
                file = open("canvas_api_token.txt", 'w')
                file.write(self.token)
                file.close()
            self.staylogged = 1
        else:
            print("here")
            if file:
                os.remove("canvas_api_token.txt")
            self.staylogged = 0
        
        print(self.staylogged, ": staylogged inside of funtion")
        settingfile = open("settings.txt", 'w')
        settingfile.write(str(self.staylogged) + "\n")
        settingfile.write(str(self.darkmode) + "\n")
        settingfile.close()

    def darkModeSwitch(self, themeswitch):
        print(themeswitch)
        if themeswitch == 1:
            self.darkmode = "dark"
            self.root.tk.call('set_theme', self.darkmode)
        else:
            self.darkmode = "light"
            self.root.tk.call('set_theme', self.darkmode)
        settingfile = open("settings.txt", 'w')
        settingfile.write(str(self.staylogged) + "\n")
        settingfile.write(str(self.darkmode) + "\n")
        settingfile.close()


    def open_popup(self):
        top = Toplevel(self.root)
        top.geometry("500x500")
        top.title("Settings")
        SLI = tk.IntVar(value=self.staylogged)
        tk.Checkbutton(top, text = "Stay Logged In", variable = SLI, onvalue=1, offvalue=0, command = lambda: self.stayLoggedIn(SLI.get())).pack()
        
        if self.darkmode == "dark":
            switch = 1
        else:
            switch = 0
        
        themeSwitch = tk.IntVar(value=switch)
        themeSwitch.set(switch)
        tk.Checkbutton(top,text= "Dark Mode", variable = themeSwitch, onvalue=1, offvalue=0, command= lambda: self.darkModeSwitch(themeSwitch.get())).pack()
    
    def getIcons(self):
        gearIcon = Image.open("canvas_gear.png")
        refreshIcon = Image.open("canvas_refresh.png")
        newSize = (25, 25)
        gearIcon = gearIcon.resize(newSize)
        refreshIcon = refreshIcon.resize(newSize)
        refreshIcon = itk.PhotoImage(refreshIcon)
        gearIcon = itk.PhotoImage(gearIcon)

        return gearIcon, refreshIcon

    def refresh(self):
        # Somehow make the model refresh
        return 0