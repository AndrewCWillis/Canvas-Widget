# -*- coding: utf-8 -*-
'''
CS498 Group Project 
A Foundation for the Graphics

'''
import canvasPractice
import tkinter as tk
from tkinter import ttk

stuCanvas = canvasPractice.userCanvas()
root = tk.Tk()
root.tk.call('lappend', 'auto_path', 'awthemes-10.4.0')
root.tk.call('package', 'require', 'awdark')
style = ttk.Style()
style.theme_use('awdark')

root.title("Canvas Widget")
root.geometry('500x500')
tabControl = ttk.Notebook(root)
  
tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
tab3 = ttk.Frame(tabControl)
tab4 = ttk.Frame(tabControl)

tabControl.add(tab1, text ='Grades')
tabControl.add(tab2, text ='Announcements')
tabControl.add(tab3, text ='Assignments')
tabControl.add(tab4, text ='To Do')

tabControl.pack(expand = 1, fill ="both")
  
ttk.Label(tab1, 
          text = stuCanvas.getGrades()).grid(column = 0, 
                               row = 0,
                               padx = 30,
                               pady = 30)  
ttk.Label(tab2,
          text = stuCanvas.getAnnouncements()).grid(column = 0,
                                    row = 0, 
                                    padx = 30,
                                    pady = 30)
ttk.Label(tab3,
          text = stuCanvas.getAnnouncements()).grid(column = 0,
                                    row = 0, 
                                    padx = 30,
                                    pady = 30)
ttk.Label(tab4,
          text = stuCanvas.getToDo()).grid(column = 0,
                                    row = 0, 
                                    padx = 30,
                                    pady = 30)
root.iconbitmap('canvas_icon.ico')
root.mainloop()