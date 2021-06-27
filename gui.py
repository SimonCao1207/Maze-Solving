import PySimpleGUI as sg
import numpy as np
import math
from maze import *

AppFont = 'Any 16'
sg.theme('DarkGrey5')
_VARS = {'cellCount': 10, 'gridSize': 400, 'canvas': False, 'window': False,
         'playerPos': [0, 0]}
# cellMAP = np.zeros((_VARS['cellCount'], _VARS['cellCount']), dtype=int)
cellSize = _VARS['gridSize']/_VARS['cellCount']


def drawGrid():
    cells = _VARS['cellCount']
    _VARS['canvas'].TKCanvas.create_rectangle(
        1, 1, _VARS['gridSize'], _VARS['gridSize'], outline='BLACK', width=1)
    for x in range(cells):
        _VARS['canvas'].TKCanvas.create_line(
            ((cellSize * x), 0), ((cellSize * x), _VARS['gridSize']),
            fill='BLACK', width=1)
        _VARS['canvas'].TKCanvas.create_line(
            (0, (cellSize * x)), (_VARS['gridSize'], (cellSize * x)),
            fill='BLACK', width=1)


def drawCell(x, y, color='GREY'):
    _VARS['canvas'].TKCanvas.create_rectangle(
        x, y, x + cellSize, y + cellSize,
        outline='BLACK', fill=color, width=1)


def placeCells(cellMAP):
    for row in range(cellMAP.shape[0]):
        for column in range(cellMAP.shape[1]):
            if(cellMAP[column][row] == 1):
                drawCell((cellSize*row), (cellSize*column))
            elif (cellMAP[column][row] == -1):
            	drawCell((cellSize*row), (cellSize*column), color="RED")
            elif (cellMAP[column][row] == 2):
            	drawCell((cellSize*row), (cellSize*column), color="BLUE")


def checkEvents(event):
    move = ''
    if len(event) == 1:
        if ord(event) == 63232:  # UP
            move = 'Up'
        elif ord(event) == 63233:  # DOWN
            move = 'Down'
        elif ord(event) == 63234:  # LEFT
            move = 'Left'
        elif ord(event) == 63235:  # RIGHT
            move = 'Right'
    # Filter key press Windows :
    else:
        if event.startswith('Up'):
            move = 'Up'
        elif event.startswith('Down'):
            move = 'Down'
        elif event.startswith('Left'):
            move = 'Left'
        elif event.startswith('Right'):
            move = 'Right'
    return move


# INIT :

def finalGUI(cellMAP, name: str="GridMaker"):
	layout = [[sg.Canvas(size=(_VARS['gridSize'], _VARS['gridSize']),
	                     background_color='white',
	                     key='canvas')],
	          [sg.Exit(font=AppFont)]]

	_VARS['window'] = sg.Window(name, layout, resizable=True, finalize=True,
	                            return_keyboard_events=True)
	_VARS['canvas'] = _VARS['window']['canvas']
	drawGrid()
	drawCell(_VARS['playerPos'][0], _VARS['playerPos'][1], 'TOMATO')
	placeCells(cellMAP)

	while True:             # Event Loop
	    event, values = _VARS['window'].read()
	    if event in (None, 'Exit'):
        	break
	_VARS['window'].close()