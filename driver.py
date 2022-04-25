'''
CS498 Group Project 
This file is the one that should be ran to start the application.

Robert Crispen
Wade Durham
Drew Willis
Spencer Gillaspie
'''

import loginScreen
import appGUI
import os
from canvasapi import Canvas

if not os.path.exists('canvas_api_token.txt'):
    verify = loginScreen.login()

widget = appGUI.widget()