# -*- coding: utf-8 -*-
'''
CS498 Group Project 
The GUI for the Canvas application.

Robert Crispen
Wade Durham
Drew Willis
Spencer Gillaspie
'''

import appBackEnd
import tkinter as tk
from tkinter import BOTH, E, LEFT, NE, NS, NW, RIGHT, TOP, VERTICAL, HORIZONTAL, W, X, Y, Toplevel, ttk
import os
from datetime import datetime
from datetime import timedelta
from dateutil import tz
from datetime import date
from PIL import Image
from PIL import ImageTk as itk
import webbrowser

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
        self.stuCanvas = appBackEnd.userCanvas(TOKEN)
        self.root = tk.Tk()
        self.days = 7
        self.root.tk.call('source', 'Azure-ttk-theme-main/Azure-ttk-theme-main/azure.tcl')
        self.root.tk.call('set_theme', self.darkmode)
        self.style = ttk.Style()

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
        self.refreshButton = tk.Button(text = "Refresh", image=self.refreshIcon, command=self.refresh)

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
        self.sb3Horiz = ttk.Scrollbar(self.tab3, orient=HORIZONTAL)
        self.sb4 = ttk.Scrollbar(self.tab4, orient=VERTICAL)
        
        # Canvas to go in the tab frames. This is so that the content can be
        #   made scrollable
        self.canvas1 = tk.Canvas(self.tab1, yscrollcommand=self.sb1.set)
        self.canvas2 = tk.Canvas(self.tab2, yscrollcommand=self.sb2.set)
        self.canvas3 = tk.Canvas(self.tab3, yscrollcommand=self.sb3.set, xscrollcommand=self.sb3Horiz.set)
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
        self.sb3Horiz.config(command=self.canvas3.xview)
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
        
    # Put the announcements onto the announcements tab     
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
                          #background = 'white',
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
        
    # Put the to-dos onto the to do tab
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
                          #background = 'white',
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
    
    # Put the next week of assignments in the Assignments tab in a calendar form
    def displayCalendar(self):
        assignments = self.stuCanvas.getAssignments() #returns ordered dictionary sorted by datetime due date keys
        idToName = self.stuCanvas.getCourseIdsToCourseName()
        Colors = self.stuCanvas.getColors()
        numDays = self.days
        today = date.today()
        dayCells = [tk.Frame(self.innerFrame3, bg = 'light gray', width = 200, height = 200) for day in range(numDays)]
        
        for i in range(numDays):
            day = today + timedelta(days=i)
            
            # Add the date as a header to each column in the calendar view
            ttk.Label(dayCells[i], 
                      text = day.strftime('%A, %m/%d/%y'), justify = 'center', background = 'gray',
                                               borderwidth = 5).grid(row = 0, column = 0, sticky = W, padx = 2)
            
            # For all the assignments that are due on this day
            key = day.strftime('%Y-%m-%d')
            if key in assignments.keys():
                for j in range(len(assignments[key])):#multiple assignments due the same day                
                    assignmentTitle = assignments[key][j][0]
                    courseId = assignments[key][j][1]
                    
                    calAssignmentString = f"{idToName[courseId]}: {assignmentTitle}"
            
                    # Add each assignment to the appropriate column/day
                    ttk.Label(dayCells[i], 
                      text = calAssignmentString, justify = 'center', background = Colors[courseId],
                                                borderwidth = 5, wraplengt=140).grid(row = 1 + j, column = 0, sticky = W, padx = 2)
            else:
                ttk.Label(dayCells[i], 
                      text = 'Nothing to Do :)',justify = 'center', background = 'light gray',
                                       borderwidth = 5, wraplengt=140).grid(row = 1, column = 0, sticky = W, padx = 2)
        r = 0 
        for i, day in enumerate(dayCells):
            if (i % 7 == 0 and i != 0) or r == 6:
                r += 1
                
            day.grid(row = r, column = (i%7), sticky = W, padx = 2) # 7 - 
 
        self.canvas3.create_window(0, 0, window=self.innerFrame3, anchor=NW) # Put the innerFrame in the canvas
        self.sb3.pack(side=RIGHT, fill=Y) # Put the scrollbar in the tab frame
        self.sb3Horiz.pack(side=TOP, fill=X)
        self.canvas3.pack(side=LEFT, anchor=NW, fill=BOTH) # Put the canvas in the tab frame
        
    # When the user toggles the Stay Logged In checkbox, do the appropriate action
    def stayLoggedIn(self, SLI):
        file = os.path.exists("canvas_api_token.txt")
        if(SLI == 1):
            if not file:
                file = open("canvas_api_token.txt", 'w')
                file.write(self.token)
                file.close()
            self.staylogged = 1
        else:
            if file:
                os.remove("canvas_api_token.txt")
            self.staylogged = 0
        
        # print(self.staylogged, ": staylogged inside of function")
        settingfile = open("settings.txt", 'w')
        settingfile.write(str(self.staylogged) + "\n")
        settingfile.write(str(self.darkmode) + "\n")
        settingfile.close()


    # When te user toggles the Dark Mode checkbox, switch the app's theme
    def darkModeSwitch(self, themeswitch):
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
    
    def changeDate(self, date):
        for widgets in self.innerFrame3.winfo_children():#deletes all the widgets in the calendar tab 
            widgets.destroy()
        self.days = 7*date #changes the amount of days that can be viewed
        self.displayCalendar() #reload the calender

    def openWebBrowser(self):
        webbrowser.open("https://uk.instructure.com/")

    # When the user clicks on the settings button, open a window with the options
    def open_popup(self):
        top = Toplevel(self.root)
        top.geometry("500x500")
        top.title("Settings")
        
        #browserButtonImage = PhotoImage(file='CanvasLogo.png')
        browserButton = tk.Button(top, text = 'Open in Browser', command = self.openWebBrowser)
        browserButton.pack(side='top')
        
        SLI = tk.IntVar(value=self.staylogged)
        tk.Checkbutton(top, text = "Stay Logged In", variable = SLI, onvalue=1, offvalue=0, command = lambda: self.stayLoggedIn(SLI.get())).pack()
        
        if self.darkmode == "dark":
            switch = 1
        else:
            switch = 0
        
        themeSwitch = tk.IntVar(value=switch)
        themeSwitch.set(switch)
        tk.Checkbutton(top,text= "Dark Mode", variable = themeSwitch, onvalue=1, offvalue=0, command= lambda: self.darkModeSwitch(themeSwitch.get())).pack()

        # Radio Buttons
        var = tk.IntVar()
        rButton = []
        text = ["1 Week", "2 Weeks", "3 Weeks"]#names for the radio buttons 
        for i in range(3):
            rButton.append(tk.Radiobutton(top, text = text[i], variable=var, value = i + 1, command=lambda: self.changeDate(var.get())))
            if self.days == ((i+1) * 7):#Check to so which button has been pressed most recently start on 7 days
                rButton[i].select()
            rButton[i].pack()
    
    # Load in the images for the refresh and settings buttons
    def getIcons(self):
        gearIcon = Image.open("canvas_gear.png")
        refreshIcon = Image.open("canvas_refresh.png")
        newSize = (25, 25)
        gearIcon = gearIcon.resize(newSize)
        refreshIcon = refreshIcon.resize(newSize)
        refreshIcon = itk.PhotoImage(refreshIcon)
        gearIcon = itk.PhotoImage(gearIcon)

        return gearIcon, refreshIcon

    # When the user clicks the refresh button, update the GUI. A new call is not
    #   being made to the API right now, so that is something that could be added
    #   later on.
    def refresh(self):
        self.displayGrades()
        self.displayAnnouncements()
        self.displayCalendar()
        self.displayTodos()