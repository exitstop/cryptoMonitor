# -*- coding: utf-8 -*- 
#https://docs.python.org/2/library/httplib.html#examples
# format() https://pyformat.info/


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

from libColorText import *
from libMyCommon import *





# API https://www.cryptopia.co.nz/Forum/Thread/255

def CryptopiaMarket(coin):	
	nonce=int(time.time())
	uri='https://www.cryptopia.co.nz/api/GetMarket/'+coin
	conn = httplib.HTTPSConnection("www.cryptopia.co.nz")	
	
	conn.request("GET", uri)

	r1 = conn.getresponse()
	# print r1.status, r1.reason
	data1 = r1.read()

	conn.close()
	# print data1
	json_parse_data = json.loads(data1)	
	# if json_parse_data['result'] == 'true':
		# print "{0:.8f}".format(json_parse_data['data']['lastDealPrice']) 
	return json_parse_data



def CryptopiaMarketMonitor(coin, upPriceBell = 999.99999999, downPriceBell = 0, avaliableHold = 0):
	exchangeName = 'cryptopia'
	jsonCryptopia = CryptopiaMarket(coin)
	lastPrice = float(jsonCryptopia['Data']['LastPrice'])
	baseVolume = float(jsonCryptopia['Data']['BaseVolume'])
	label = jsonCryptopia['Data']['Label']		
	return {"exchangeName":exchangeName,"label":label,"lastPrice":lastPrice, "upPriceBell":upPriceBell, "downPriceBell":downPriceBell, "avaliableHold":avaliableHold}