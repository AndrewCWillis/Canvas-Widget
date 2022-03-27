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
import canvasPractice
import tkinter as tk
from tkinter import BOTH, E, LEFT, NW, RIGHT, VERTICAL, W, Y, ttk
import os
from canvasapi import Canvas

class widget:
    def __init__(self):
        self.URL = 'https://uk.instructure.com'
        file = open('canvas_api_token.txt', 'r')
        TOKEN = file.readline()
        file.close()
        self.stuCanvas = canvasPractice.userCanvas(TOKEN)
        self.root = tk.Tk()
        #root.tk.call('lappend', 'auto_path', 'Azure-ttk-theme-main/azure dark')
        #root.tk.call('package', 'require', 'azure dark')
        self.root.tk.call('source', 'Azure-ttk-theme-main/Azure-ttk-theme-main/azure.tcl')
        self.root.tk.call('set_theme', 'light')
        self.style = ttk.Style()
        #style.theme_use('dark')
        #root.tk.call('lappend', 'auto_path', 'awthemes-10.4.0')
        #root.tk.call('package', 'require', 'awdark')


        self.root.title("Canvas Widget")
        self.root.geometry('500x500')
        self.tabControl = ttk.Notebook(self.root)

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
                              func=lambda x: self.canvas1.configure(scrollregion=self.canvas1.bbox("all"), width=self.innerFrame1.winfo_width()))
        self.innerFrame2.bind('<Configure>', 
                              func=lambda x: self.canvas2.configure(scrollregion=self.canvas2.bbox("all"), width=self.innerFrame2.winfo_width()))

        # Tell the scrollbars the function to execute when they are changed
        self.sb1.config(command=self.canvas1.yview)
        self.sb2.config(command=self.canvas2.yview)
        self.sb3.config(command=self.canvas3.yview)
        self.sb4.config(command=self.canvas4.yview)
        
        self.tabControl.pack(expand = 1, fill ="both")

        self.displayGrades()
        self.displayAnnouncements()

        ttk.Label(self.tab3,
                  text = self.stuCanvas.getAnnouncements()).grid(column = 0,
                                    row = 0, 
                                    padx = 30,
                                    pady = 30)
        ttk.Label(self.tab4,
                  text = self.stuCanvas.getToDo()).grid(column = 0,
                                    row = 0, 
                                    padx = 30,
                                    pady = 30)
        self.root.iconbitmap('canvas_icon.ico')
        self.root.mainloop()


        
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
