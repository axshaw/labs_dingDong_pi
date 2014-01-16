#!/usr/bin/python
import RPi.GPIO as G	# reference the GPIO Library
import time
import json
import urllib2

G.setmode(G.BCM)	# use the 'BCM' numbering scheme for pins

ledPin = 17
buttonPin = 25

G.setup(ledPin, G.OUT, pull_up_down=G.PUD_UP)		# Set pin 17 as Output
G.output(ledPin, False)
G.setup(buttonPin, G.IN, pull_up_down=G.PUD_DOWN)	# Set pin 23 as Input

lastButtonState = 0

while (True):
	buttonState = G.input(buttonPin)

	if ((lastButtonState != buttonState) and  buttonState):
		G.output(ledPin, True)
		url = 'https://api.parse.com/1/push'
		data = '{"where":{},"data":{"alert":"Hello, World!","badge":1,"sound":"doorbell-1.wav","ID":"HvedQbm6Ka"}}'
		method = 'POST'
		handler = urllib2.HTTPHandler()
		opener = urllib2.build_opener(handler)
		request = urllib2.Request(url,data)
		request.add_header('X-Parse-Application-Id','rH4WNF3YUWEl0PtcmjQj40oIviGTHHoxPqgD0loS')
		request.add_header('X-Parse-REST-API-Key','NKhmi1B1siNIj4Rd9rTDy1CeuwfticqfX1i6Js5R')
		request.add_header('Content-Type','application/json')
		request.get_method = lambda: method
		opener.open(request)
		time.sleep(2)
		print 'Button Pressed'
	else:
		G.output(ledPin, False)

	lastButtonState = buttonState

	time.sleep(0.1)

G.cleanup()		# Tidy up after outselves so we don't generate warning next time we run this
