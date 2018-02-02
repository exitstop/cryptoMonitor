# -*- coding: utf-8 -*- 
#https://docs.python.org/2/library/httplib.html#examples
# format() https://pyformat.info/
# японские свечи http://www.jqchart.com/jquery/chart/FinancialCharts/SkipEmptyDays
# candlestick chart js https://developers.google.com/chart/interactive/docs/gallery/candlestickchart

import time
import hmac
import hashlib
import json
import httplib, urllib
import sys
#определяет ширину консоли
import curses
import datetime
# from datetime import datetime, date, time
from datetime import datetime, date


import matplotlib.pyplot as plt
import numpy as np
from matplotlib.dates import num2date

from time import sleep


# import matplotlib
# matplotlib.use('TkAgg')
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
import multiprocessing

import random
from Tkinter import *
from pygame import mixer
from gtts import gTTS


from libCryptopia import *
from libBinance import *
from libMyCommon import *

tableListSort = ["index","func","coin","lastPrice","upPriceBell","downPriceBell","avaliableHold"]
tableListSortAccept = ["upPriceBell","downPriceBell","avaliableHold"]


# https://www.programcreek.com/python/example/4550/curses.A_STANDOUT
# https://docs.python.org/2/library/curses.html
class TableConteiner:
	showBank = []
	swapBank = []
	monitorSettings = []
	indexY = 0
	indexX = 0
	rocket = {"price": 0, "cout": 0}
	def down(self):
		if len(self.swapBank) - 1 > self.indexY:
			self.indexY = self.indexY + 1
	def up(self):
		if 0 < self.indexY:
			self.indexY = self.indexY - 1
	def left(self):
		if 0 < self.indexX:
			self.indexX = self.indexX - 1
	def right(self):
		if 7 > self.indexX:
			self.indexX = self.indexX + 1
	def inc(self):
		# pass
		print tableListSort[self.indexX]
		if tableListSort[self.indexX] in tableListSortAccept:
			self.monitorSettings[self.indexY][tableListSort[self.indexX]] = self.monitorSettings[self.indexY][tableListSort[self.indexX]] + 0.00000001
			self.out()
	def dec(self):
		print tableListSort[self.indexX]
		if tableListSort[self.indexX] in tableListSortAccept:
			self.monitorSettings[self.indexY][tableListSort[self.indexX]] = self.monitorSettings[self.indexY][tableListSort[self.indexX]] - 0.00000001
			self.out()
		# if self.indexX > 1 and self.indexX < 4:
		# 	self.monitorSettings[self.indexY][tableListSort[self.indexX]] = self.monitorSettings[self.indexY][tableListSort[self.indexX]] - 0.00000001
		# 	self.out()
	def addCoin(func, coin, upPriceBell = 9999999, downPriceBell = 0, avaliableHold = 0, coeffUp = 1.05, coeffDown = 0.95):
		table.monitorSettings.append({"func": func, "coin": coin, "upPriceBell" : upPriceBell, "downPriceBell" : downPriceBell, "avaliableHold" : avaliableHold,	"coeffUp": coeffUp, "coeffDown": coeffDown})

	def connect(self):
		for item in self.monitorSettings:
			self.showBank.append(  item["func"](coin = item["coin"], upPriceBell = item["upPriceBell"], downPriceBell = item["downPriceBell"], avaliableHold = item["avaliableHold"] ) )
		self.swap()
		self.rocket["cout"] = self.rocket["cout"] + 1

	def out(self):
		stdscr.clear()
		lIndex = 0
		for Item in self.swapBank:
			Item.update({"index":lIndex})

			Item['upPriceBell'] = self.monitorSettings[lIndex]["upPriceBell"]
			Item['downPriceBell'] = self.monitorSettings[lIndex]["downPriceBell"]
			Item['avaliableHold'] = self.monitorSettings[lIndex]["avaliableHold"]

			color=[0,3,3,0,3,3,0]
			if Item["lastPrice"] >= Item["upPriceBell"]:
				PlaySound(soundSirenaFile, sirenaSecond)
				color=[2 for i in range(7)] 
			elif Item["lastPrice"] <=  Item["downPriceBell"]:
				PlaySound(soundSirenaFile1, sirenaSecond)
				color=[1 for i in range(7)]

			if self.rocket["cout"] >= 12 or self.rocket["cout"] >= 24 or self.rocket["cout"] >= 60:
				self.rocket["cout"] = 0
				if rocket["price"] <= Item["lastPrice"] * Item["coeffUp"]:
					PlaySound(soundSirenaFile2, sirenaSecond2)
				elif rocket["price"] >= Item["lastPrice"] * Item["coeffDown"]:
					PlaySound(soundSirenaFile1, sirenaSecond)	
			
			# if lIndex == self.indexY:
			# 	color = [4 for i in range(7)]
			# 	color[self.indexX] = 2
			PrintLine(Item, color = color)
			lIndex += 1
		stdscr.refresh()

	def swap(self):
		del self.swapBank[:]
		self.swapBank = self.showBank[:]
	def clearBank(self):
		self.swap()
		del self.showBank[:]



table = TableConteiner()

ex = {"ctrl": 0, "c": 0}


def on_press(key):
	global table
	global ex
	try:
		print('{0} press\n'.format(key))
		# print('alphanumeric key {0} pressed\n'.format(key.char))	
		if key == keyboard.Key.ctrl:
			# Stop listener

			ex['ctrl'] = 1
			# sys.exit()
		elif key.char == 'q':
			# ex['c'] = 1
			if ex['ctrl'] == 1:
				PlaySound("sound/R2D2.ogg", 2)
				sleep(2)
				sys.exit()
		elif key == keyboard.Key.up:
			table.up()
		elif key == keyboard.Key.down:
			table.down()
		elif key == keyboard.Key.right:
			table.right()
		elif key == keyboard.Key.left:
			table.left()
		else:
			ex['ctrl'] = 0
	except AttributeError:
		print('special key {0} pressed'.format(
		           key))
		pass
		# print('special key {0} pressed'.format(	key))
	table.out()

def on_release(key):
	global table
	global ex
	print('{0} released\n'.format(key))
	try:
		if key == keyboard.Key.esc:
			pass
		elif key.char == '=':
			table.inc()
		elif key.char== '-':
			table.dec()
		elif key == keyboard.Key.ctrl:
			ex['ctrl'] = 0
	except AttributeError:
		# print('special key {0} pressed'.format(	key))
		pass




def ThreadMonitor():
	global table
	# table.monitorSettings.append({"func": CryptopiaMarketMonitor, 	"coin": 'HOLD_BTC',	"upPriceBell" : 0.00000550, 	"downPriceBell" : 0.00000430, 	"avaliableHold" : 52006.50456414,	"coeffUp": 1.15, "coeffDown": 0.85})
	# table.monitorSettings.append({"func": BinanceMarketMonitor, 	"coin": 'GTOBTC',	"upPriceBell" : 9.0	, 			"downPriceBell" : 0, 			"avaliableHold" : 0, 				"coeffUp": 1.05, "coeffDown": 0.95})
	# table.monitorSettings.append({"func": BinanceMarketMonitor, 	"coin": 'BCDBTC',	"upPriceBell" : 9.0, 			"downPriceBell" : 0, 			"avaliableHold" : 0,				"coeffUp": 1.05, "coeffDown": 0.95})
	# table.monitorSettings.append({"func": BinanceMarketMonitor, 	"coin": 'BTCUSDT',	"upPriceBell" : 99999, 			"downPriceBell" : 0, 			"avaliableHold" : 0,				"coeffUp": 1.05, "coeffDown": 0.95})

	table.addCoin(func = CryptopiaMarketMonitor, 	coin = 'HOLD_BTC', upPriceBell = 0.00000550, downPriceBell = 0.00000430, avaliableHold = 52006.50456414, coeffUp = 1.15, coeffDown = 0.85)
	table.addCoin(func = BinanceMarketMonitor, 	 	coin = 'GTOBTC',  coeffUp = 1.15, coeffDown = 0.85)
	table.addCoin(func = BinanceMarketMonitor,		coin = 'BCDBTC',  coeffUp = 1.15, coeffDown = 0.85)
	table.addCoin(func = BinanceMarketMonitor,		coin = 'BTCUSDT', coeffUp = 1.15, coeffDown = 0.85)

	while True:
		try:
			# clear()
			table.connect()
			table.out()
			

			# print '──────────────────────────────────────────────────────────────────────────────────────'
			sleep(timeOut)
			table.clearBank()

		except (KeyboardInterrupt, SystemExit):
			sys.exit()
			raise
		except  Exception as inst:
			print type(inst)     # the exception instance
			print inst.args      # arguments stored in .args
			print inst   
			print "Except"
	
# https://pythonworld.ru/web/cgi-1.html
from http.server import HTTPServer, CGIHTTPRequestHandler
# from pynput import keyboard



# curses.nocbreak(); stdscr.keypad(0); curses.echo()


def main():

	# while True:

	# server_address = ("", 8000)
	# httpd = HTTPServer(server_address, CGIHTTPRequestHandler)
	# httpd.serve_forever()

	f = threading.Thread(target=ThreadMonitor)
	f.daemon = True
	f.start()

	# # Collect events until released
	with keyboard.Listener(	on_release	=	on_release,
							on_press	=	on_press
			) as listener:
		listener.join()


	# price_check_gate_io('qash_eth')
	# f = FirstThread_monitor_price()
	# f = FirstThread_monitor_ticket()
	# f.daemon = True
	# f.start()

main()


