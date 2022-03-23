# -*- coding: utf-8 -*-
'''
CS498 Group Project 
A Foundation for the Graphics
'''
import enum
from itertools import count
from operator import countOf
import canvasPractice
import tkinter as tk
from tkinter import W, ttk
import os
from canvasapi import Canvas

class widget:
    def __init__(self):
        self.URL = 'https://uk.instructure.com'
        self.stuCanvas = canvasPractice.userCanvas()
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
    
        for i in range(len(gradesList)):
            ttk.Label(self.tab1, 
                      text = '{}: {}'.format(idToName[gradesList[i]['class']], gradesList[i]['grade']),
                      justify = 'left',
                      background = Colors[gradesList[i]['class']],
                      borderwidth = 5,
                      relief = 'raised').grid(column = 0, 
                               row = i,
                               padx = 10,
                               pady = 10,
                               sticky = W)
          
    def displayAnnouncements(self):
        announcementsDict = self.stuCanvas.getAnnouncements()
        idToName = self.stuCanvas.getCourseIdsToCourseName()
        Colors = self.stuCanvas.getColors()
        countOfRows = 0 # Counter for which row to place the next item
    
        # For every course there is an announcement for
        for courseKey in announcementsDict:
        # Put the class name as a 'header' of sorts
            ttk.Label(self.tab2, 
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
                ttk.Label(self.tab2, 
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

