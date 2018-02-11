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
from libKucoin import *
from libGate import *
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
		#   self.monitorSettings[self.indexY][tableListSort[self.indexX]] = self.monitorSettings[self.indexY][tableListSort[self.indexX]] - 0.00000001
		#   self.out()
	def addCoin(self, func = 0, coin = 0, upPriceBell = 99999.0, downPriceBell = 0, avaliableHold = 0, coeffUp = 1.03 , coeffDown = 0.97 ):
		table.monitorSettings.append({"func": func, "coin": coin, "upPriceBell" : upPriceBell, "downPriceBell" : downPriceBell, "avaliableHold" : avaliableHold,    "coeffUp": coeffUp, "coeffDown": coeffDown, 'rocketPrice': 0})

	def connect(self):      
		lIndex = 0

		
		for item in self.monitorSettings:
			try:
				dT = item["func"](coin = item["coin"], upPriceBell = item["upPriceBell"], downPriceBell = item["downPriceBell"], avaliableHold = item["avaliableHold"]) 
				dictTemp = {"exchangeName":dT['exchangeName'],"label":dT['label'],"lastPrice":dT['lastPrice'], 
							"upPriceBell":dT['upPriceBell'], "downPriceBell":dT['downPriceBell'], 
							"avaliableHold":dT['avaliableHold'], "coeffUp": item['coeffUp'], "coeffDown": item['coeffDown']}
				self.showBank.append( dictTemp )


			except  Exception as inst:
				PrintFrameError(inst)
				stdscr.addstr("\n")
				print "Unexpected error2:", sys.exc_info()[0]
				raise  
			
		self.swap()
		self.rocket["cout"] = self.rocket["cout"] + 1

	def out(self):
		stdscr.clear()
		lIndex = 0
		playSound = 0
		if len(self.swapBank) <= 0:
			return
		for Item in self.swapBank:
			try:
				Item.update({"index":lIndex})

				color=[0,3,3,0,3,3,0]
				# if self.rocket["cout"] == 2:
				#   Item["lastPrice"] = Item["lastPrice"] * Item["coeffDown"]

				if self.rocket["cout"] == 1:
					self.monitorSettings[lIndex]["rocketPrice"] = Item["lastPrice"]
				elif self.rocket["cout"] >= 2 or self.rocket["cout"] >= 24 or self.rocket["cout"] >= 60:
					if self.rocket["cout"] >= 60:
						self.rocket["cout"] = 0
					if self.monitorSettings[lIndex]["rocketPrice"] * Item["coeffUp"] <= Item["lastPrice"] :
						color=[2 for i in range(7)] 
						# PlaySound(soundSirenaFile2, sirenaSecond2)                  
					elif self.monitorSettings[lIndex]["rocketPrice"] * Item["coeffDown"] >= Item["lastPrice"]:
						color=[1 for i in range(7)]
						# PlaySound(soundSirenaFile1, sirenaSecond)


				Item['upPriceBell'] = self.monitorSettings[lIndex]["rocketPrice"] * Item["coeffUp"]
				Item['downPriceBell'] = self.monitorSettings[lIndex]["rocketPrice"] * Item["coeffDown"]
				# Item['upPriceBell'] = self.monitorSettings[lIndex]["upPriceBell"]
				# Item['downPriceBell'] = self.monitorSettings[lIndex]["downPriceBell"]
				Item['avaliableHold'] = self.monitorSettings[lIndex]["avaliableHold"]

				
				if Item["lastPrice"] >= Item["upPriceBell"]:
					playSound = 1
					color=[2 for i in range(7)] 
				elif Item["lastPrice"] <=  Item["downPriceBell"]:
					playSound = 2
					color=[1 for i in range(7)]

				

				
				# if lIndex == self.indexY:
				#   color = [4 for i in range(7)]
				#   color[self.indexX] = 2
				PrintLine(Item, color = color)
				lIndex += 1
			except  Exception as inst:
				PrintFrameError(inst)
				print "Unexpected error1:", sys.exc_info()[0]
				raise 
		# stdscr.addstr(lIndex, 0, str("exit: ctrl+q"), curses.color_pair(0))
		if playSound == 1:
			PlaySound(soundSirenaFile, sirenaSecond)
		elif playSound == 2:
			PlaySound(soundSirenaFile1, sirenaSecond)
		stdscr.addstr("\n")
		stdscr.refresh()
	def resetAlert(self):
		lIndex = 0
		if len(self.swapBank) <= 0:
			return
		for Item in self.swapBank:
			try:
				self.monitorSettings[lIndex]["rocketPrice"] = Item["lastPrice"]
				lIndex += 1
			except  Exception as inst:
				PrintFrameError(inst)
				print "Unexpected error4:", sys.exc_info()[0]
				raise 

	def swap(self):
		del self.swapBank[:]
		self.swapBank = self.showBank[:]
	def clearBank(self):
		self.swap()
		del self.showBank[:]



table = TableConteiner()

ex = {"ctrl": 0, "c": 0}


def ThreadMonitor():
	global table
	# table.monitorSettings.append({"func": CryptopiaMarketMonitor,     "coin": 'HOLD_BTC', "upPriceBell" : 0.00000550,     "downPriceBell" : 0.00000430,   "avaliableHold" : 52006.50456414,   "coeffUp": 1.15, "coeffDown": 0.85})
	# table.monitorSettings.append({"func": BinanceMarketMonitor,   "coin": 'GTOBTC',   "upPriceBell" : 9.0 ,           "downPriceBell" : 0,            "avaliableHold" : 0,                "coeffUp": 1.05, "coeffDown": 0.95})
	# table.monitorSettings.append({"func": BinanceMarketMonitor,   "coin": 'BCDBTC',   "upPriceBell" : 9.0,            "downPriceBell" : 0,            "avaliableHold" : 0,                "coeffUp": 1.05, "coeffDown": 0.95})
	# table.monitorSettings.append({"func": BinanceMarketMonitor,   "coin": 'BTCUSDT',  "upPriceBell" : 99999,          "downPriceBell" : 0,            "avaliableHold" : 0,                "coeffUp": 1.05, "coeffDown": 0.95})

	# total (HOLD) 52006.50456414 + 4920.296464350002 = 56926.80102849
	table.addCoin( func = CryptopiaMarketMonitor,   coin = 'HOLD_BTC', upPriceBell =0.00000550,  downPriceBell = 0.00000430, avaliableHold = 56926.80102849 , coeffUp =1.10, coeffDown =0.90)
	table.addCoin( BinanceMarketMonitor,    'BTCUSDT')
	table.addCoin( BinanceMarketMonitor,    'GTOBTC')
	# table.addCoin( BinanceMarketMonitor,    'AIONBTC')
	# table.addCoin( BinanceMarketMonitor,    'BCDBTC', coeffUp = 1.05, coeffDown = 0.95)
	table.addCoin( KucoinMarketMonitor,     'ZPT-BTC', coeffUp = 1.10, coeffDown = 0.90, avaliableHold = 2163 )
	table.addCoin( KucoinMarketMonitor,     'KEY-BTC', coeffUp = 1.10, coeffDown = 0.90, avaliableHold = 10064 )
	# table.addCoin( KucoinMarketMonitor,     'OCN-BTC', coeffUp = 1.10, coeffDown = 0.90)
	# table.addCoin( KucoinMarketMonitor,     'COFI-BTC', coeffUp = 1.15, coeffDown = 0.85)
	# table.addCoin( GateMarketMonitor,       'jnt_usdt', coeffUp = 1.05, coeffDown = 0.95)
	# table.addCoin( GateMarketMonitor,       'nas_usdt', coeffUp = 1.05, coeffDown = 0.95)
	print("get price...")
	stdscr.addstr("\n")

	while True:
		try:
			# clear()
			table.connect()
			table.out()
			

			# print '──────────────────────────────────────────────────────────────────────────────────────'
			sleep(timeOut)
			table.clearBank()

		except  Exception as inst:
			PrintFrameError(inst)
	
# https://pythonworld.ru/web/cgi-1.html
# from http.server import HTTPServer, CGIHTTPRequestHandler
# from pynput import keyboard



# curses.nocbreak(); stdscr.keypad(0); curses.echo()




def keyb():
	global stdscr
	# stdscr.nodelay(True)
	key=""
	# stdscr.clear()                
	# stdscr.addstr("Detected key:")
	while 1:          
		try:                 
			key = stdscr.getkey()         
			# stdscr.clear()                
			# stdscr.addstr("Detected key:")
			stdscr.addstr(str(key))
			if key == 'q':
				PlaySound("sound/R2D2.ogg", 2);	sleep(2)
				curses.endwin()
				sys.exit()
			elif key == 'a':
				PlaySound("sound/nemeckaja-rech-i-signal-trevogi.ogg", 8);	sleep(8)
			elif key == 'r':
				table.resetAlert()
			elif key == os.linesep:
				break           
		except Exception as inst:
		   PrintFrameError(inst)
		   pass   


def main():
	# while True:

	# server_address = ("", 8000)
	# httpd = HTTPServer(server_address, CGIHTTPRequestHandler)
	# httpd.serve_forever()

	f = threading.Thread(target=ThreadMonitor)
	f.daemon = True
	f.start()


	f = threading.Thread(target=keyb)
	f.start()

	# # Collect events until released
	# with keyboard.Listener(   on_release  =   on_release,
	#                       on_press    =   on_press
	#       ) as listener:
	#   listener.join()


	# price_check_gate_io('qash_eth')
	# f = FirstThread_monitor_price()
	# f = FirstThread_monitor_ticket()
	# f.daemon = True
	# f.start()



main()







