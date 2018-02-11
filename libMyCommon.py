# -*- coding: utf-8 -*- 

import os
from pygame import mixer
from time import sleep
import threading
import curses
from pynput import keyboard
import inspect

# https://pyformat.info/
outFormat1 		 = '│{:^15}│{:^10}│{:^15.8f}'
soundSirenaFile  = 'sound/2-sirena-temnoe-vremya.ogg'
soundSirenaFile1 = 'sound/obj_belltower.ogg'
soundSirenaFile2 = 'sound/starcraft-2-obnaruzhen-zapusk-yadernoy-rakety.ogg'
sirenaSecond 	= 5
sirenaSecond2 	= 5
timeOut 		= 5
coeffPrice		= 1.15

# utf-8 sumbols https://unicode-table.com/ru/#box-drawing
# textUp = "∧ "
# textDown = " ∨ "
# textUp = "⩞ "
# textDown = " ⩣ "
# textUp = "↑ "
# textDown = " ↓ "
textUp = "⟙ "
textDown = " ⟘ "

clear = lambda: os.system('clear')


# thread python https://www.ibm.com/developerworks/ru/library/l-python_part_9/index.html
def PlaySoundThread(file, time):
	mixer.init()
	mixer.music.load(file)
	mixer.music.play()
	sleep(time)
	mixer.quit()


def PlaySound(file, time):
	t = threading.Thread(target=PlaySoundThread, args=(file, time))
	t.daemon = True
	t.start()



stdscr = curses.initscr()
# curses.noecho()
# curses.cbreak()



curses.start_color()
curses.use_default_colors()

curses.init_pair(0, curses.COLOR_WHITE, -1)
curses.init_pair(1, curses.COLOR_RED, -1)
curses.init_pair(2, curses.COLOR_GREEN, -1)
curses.init_pair(3, 0x66, -1)
curses.init_pair(4, 0x44, -1)

# https://www.programcreek.com/python/example/4550/curses.A_STANDOUT
# https://docs.python.org/2/library/curses.html
def PrintLine(date, color = 0):
	if color == 0:
		color=[0,0,0,0,0,0,0]
	fFormat = "8"
	if date["lastPrice"] >= 10:
		fFormat = "2"
	xIndex = 0
	stdscr.addstr(int(date["index"]), xIndex, str(date["index"]), curses.color_pair(color[0]))
	xIndex += 3
	stdscr.addstr(int(date["index"]), xIndex, str(date["exchangeName"]), curses.color_pair(color[1]))
	xIndex += 15
	stdscr.addstr(int(date["index"]), xIndex, str(date["label"]), curses.color_pair(color[2]))
	xIndex += 10
	stdscr.addstr(int(date["index"]), xIndex, str(("{:^15."+fFormat+"f}").format(date["lastPrice"])), curses.color_pair(color[3]))
	xIndex += 15
	if date["upPriceBell"]!= 99999:
		stdscr.addstr(int(date["index"]), xIndex, str(("⟙{:^15."+fFormat+"f}").format(date["upPriceBell"])), curses.color_pair(color[4]))
	xIndex += 15
	if date["downPriceBell"]!= 0:
		stdscr.addstr(int(date["index"]), xIndex, str(("⟘{:^15."+fFormat+"f}").format(date["downPriceBell"])), curses.color_pair(color[5]))
	xIndex += 15
	if date["avaliableHold"]!= 0:
		stdscr.addstr(int(date["index"]), xIndex, str("{:^15}".format(date["avaliableHold"]*date["lastPrice"])), curses.color_pair(color[6]))


def PrintFrameError(inst):
  callerframerecord = inspect.stack()[1]
  frame = callerframerecord[0]
  info = inspect.getframeinfo(frame)
  print type(inst) 
  stdscr.addstr("\n")
  print inst.args
  stdscr.addstr("\n")
  print info.filename + " " + info.function + " " + str(info.lineno)
  stdscr.addstr("\n")
  PlaySound("sound/zvuk_bjushhegosja_stekla.ogg", 2); sleep(2)
  

