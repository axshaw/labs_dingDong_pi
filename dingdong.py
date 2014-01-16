#!/usr/bin/python
import RPi.GPIO as G	# reference the GPIO Library
import os
import subprocess
import time
import json
import uuid
import httplib

G.setmode(G.BCM)	# use the 'BCM' numbering scheme for pins

statusPin = 23
runningPin = 24

ledPin = 17
buttonPin = 25

G.setup(statusPin, G.OUT, pull_up_down=G.PUD_UP)
G.output(statusPin, False)
G.setup(runningPin, G.OUT, pull_up_down=G.PUD_UP)
G.output(runningPin, True)

G.setup(ledPin, G.OUT, pull_up_down=G.PUD_UP)		# Set pin 17 as Output
G.output(ledPin, False)
G.setup(buttonPin, G.IN, pull_up_down=G.PUD_DOWN)	# Set pin 23 as Input

lastButtonState = 0

while (True):
	G.output(statusPin, True)
	G.output(runningPin, False)

	buttonState = G.input(buttonPin)

	if ((lastButtonState != buttonState) and  buttonState):
		G.output(runningPin, True)
		G.output(ledPin, True)
		subprocess.Popen(['mpg321','-g','100','/home/pi/doorbell-1.mp3'],stdin=None, stdout=None, stderr=None, close_fds=True)
		filename = str(uuid.uuid4()) + '.jpg'

		subprocess.call(['fswebcam', '-S2', '-r', '960x720', '--rotate', '270', '-d', '/dev/video0', filename])

		connection = httplib.HTTPSConnection('api.parse.com', 443)
		connection.connect()
		connection.request('POST', '/1/files/pic.jpg', open(filename, 'r'), {
       			"X-Parse-Application-Id": "rH4WNF3YUWEl0PtcmjQj40oIviGTHHoxPqgD0loS",
       			"X-Parse-REST-API-Key": "NKhmi1B1siNIj4Rd9rTDy1CeuwfticqfX1i6Js5R",
       			"Content-Type": "image/jpeg"
     		})
		result = json.loads(connection.getresponse().read())
		objectId = result['name']

		connection = httplib.HTTPSConnection('api.parse.com', 443)
		connection.connect()
		connection.request('POST', '/1/classes/knocker', json.dumps({
       			"imageFile": {
         			"name": objectId,
         			"__type": "File"
       			}
     		}), {
       			"X-Parse-Application-Id": "rH4WNF3YUWEl0PtcmjQj40oIviGTHHoxPqgD0loS",
       			"X-Parse-REST-API-Key": "NKhmi1B1siNIj4Rd9rTDy1CeuwfticqfX1i6Js5R",
       			"Content-Type": "application/json"
     		})
		result = json.loads(connection.getresponse().read())
		print result
		objectId = result['objectId']

		connection = httplib.HTTPSConnection('api.parse.com', 443)
		connection.connect()
		connection.request('POST', '/1/push', json.dumps({
       			"where": {},
       			"data": {
         			"alert": "There is somebody at the door",
				"badge": 1,
				"sound": "doorbell-1.wav",
				"ID": objectId
       			}
     		}), {
       			"X-Parse-Application-Id": "rH4WNF3YUWEl0PtcmjQj40oIviGTHHoxPqgD0loS",
       			"X-Parse-REST-API-Key": "NKhmi1B1siNIj4Rd9rTDy1CeuwfticqfX1i6Js5R",
       			"Content-Type": "application/json"
     		})
		result = json.loads(connection.getresponse().read())
		print result

		os.remove(filename)

		print 'Button Pressed'
	else:
		G.output(ledPin, False)

	lastButtonState = buttonState

	time.sleep(0.1)

G.cleanup()		# Tidy up after outselves so we don't generate warning next time we run this
