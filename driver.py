'''
CS498 Group Project 
A Foundation for the Graphics
'''
import canvasPractice
import loginScreen
import graphicsBasic
import os
from canvasapi import Canvas

if not os.path.exists('canvas_api_token.txt'):
    verify = loginScreen.login()

widget = graphicsBasic.widget()