# -*- coding: utf-8 -*-
'''
CS498 Group Project 
A Foundation for the Graphics

'''
import canvasPractice
import tkinter as tk
from tkinter import ttk

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
  
tabControl.add(tab1, text ='Grades')
tabControl.add(tab2, text ='Tab 2')
tabControl.pack(expand = 1, fill ="both")
  
ttk.Label(tab1, 
          text ="Welcome to Canvas").grid(column = 0, 
                               row = 0,
                               padx = 30,
                               pady = 30)  
ttk.Label(tab2,
          text ="Blah").grid(column = 0,
                                    row = 0, 
                                    padx = 30,
                                    pady = 30)
root.iconbitmap('canvas_icon.ico')
root.mainloop()