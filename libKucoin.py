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



def KucoinMarket(coin):	
	nonce=int(time.time())
	uri='https://api.kucoin.com/v1/open/tick?symbol='+coin
	conn = httplib.HTTPSConnection("api.kucoin.com")		
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


# {"success":true,"code":"OK","msg":"Operation succeeded.","timestamp":1517757936115,"data":{"coinType":"ZPT","trading":true,"symbol":"ZPT-NEO","lastDealPrice":9.55E-4,
# "buy":9.55E-4,"sell":9.56E-4,"change":-4.3E-5,"coinTypePair":"NEO","sort":0,"feeRate":0.001,"volValue":68105.64636727,"high":0.001041,"datetime":1517757934000,
# "vol":7.1414813384E7,"low":8.8E-4,"changeRate":-0.0431}}
def KucoinMarketMonitor(coin, upPriceBell = 999.99999999, downPriceBell = 0, avaliableHold = 0):
	exchangeName = 'kucoin'
	jsonReturn = KucoinMarket(coin)
	lastPrice = float(jsonReturn['data']['lastDealPrice'])
	label = jsonReturn['data']['symbol']
	# volValue = jsonReturn['data']['volValue']
	return {"exchangeName":exchangeName,"label":label,"lastPrice":lastPrice, "upPriceBell":upPriceBell, "downPriceBell":downPriceBell, "avaliableHold":avaliableHold}
