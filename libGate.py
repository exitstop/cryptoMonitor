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

import multiprocessing

import random
from Tkinter import *
from pygame import mixer
from gtts import gTTS

import socket


from libColorText import *
from libMyCommon import *

#  https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md



def GateMarket(coin):	
	nonce=int(time.time())
	uri='http://data.gate.io/api2/1/ticker/'+coin
	conn = httplib.HTTPSConnection("data.gate.io")		
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


# {"result":"true","last":8439,"lowestAsk":8473,"highestBid":8437.03,"percentChange":-7.9039301310044,"baseVolume":5028306.22,"quoteVolume":562.78,"high24hr":9480,"low24hr":8401}
def GateMarketMonitor(coin, upPriceBell = 999.99999999, downPriceBell = 0, avaliableHold = 0):
	exchangeName = 'gate'
	jsonReturn = GateMarket(coin)
	lastPrice = float(jsonReturn['last'])
	label = coin
	# volValue = jsonReturn['data']['volValue']
	return {"exchangeName":exchangeName,"label":label,"lastPrice":lastPrice, "upPriceBell":upPriceBell, "downPriceBell":downPriceBell, "avaliableHold":avaliableHold}
