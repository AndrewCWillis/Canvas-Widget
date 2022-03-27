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

class login:
    def __init__(self):
        self.URL = 'https://uk.instructure.com'
        self.login = tk.Tk() 
        self.login.title("Login Window")
        self.login.geometry('250x200')
        self.authSucc = False
        self.login.tk.call('source', 'Azure-ttk-theme-main/Azure-ttk-theme-main/azure.tcl')
        self.login.tk.call('set_theme', 'light')
        style = ttk.Style()
                
        self.canvas1 = tk.Canvas(self.login, width = 250, height = 200,  relief = 'raised')
        self.canvas1.pack()
        self.label1 = ttk.Label(self.login, text='Please, paste your token below')
        self.canvas1.create_window(125, 50, window=self.label1)
                
        self.entry1 = ttk.Entry (self.login)
        self.canvas1.create_window(125, 90, window=self.entry1)
            
        self.button = ttk.Button(self.login, text = "Submit", command = self.verifyToken)
        self.canvas1.create_window(125,130,window=self.button)
        self.login.iconbitmap('canvas_icon.ico')
        self.login.mainloop()

    def verifyToken(self):
    
        text = self.entry1.get()
        test = Canvas(self.URL, text)
        try:
            self.authSucc = True
            test.get_current_user()
        except:
            self.authSucc = False
            self.label1.config(text = 'Invalid Access Token', fg = 'red', font = 14)
            print(text)
        
        if self.authSucc:
            if not os.path.exists('canvas_api_token.txt'):
                print('no key stored')
                file = open('canvas_api_token.txt', 'w')
                file.write(text)
                file.close()
            else:
                print('Key previously stored')
                
            self.login.destroy()


   


