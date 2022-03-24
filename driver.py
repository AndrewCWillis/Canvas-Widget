'''
CS498 Group Project 
A Foundation for the Graphics
'''
import canvasPractice
import loginScreen
import graphicsBasic
import os
from canvasapi import Canvas

if os.environ.get('Canvas_Key') is None:
    verify = loginScreen.login()

widget = graphicsBasic.widget()