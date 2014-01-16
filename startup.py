import RPi.GPIO as G
import time
import os

statusPin = 23
runningPin = 24

while True:
	G.setmode(G.BCM)
	G.setup(statusPin, G.OUT, pull_up_down=G.PUD_UP)
	G.setup(runningPin, G.OUT, pull_up_down=G.PUD_UP)

	G.output(statusPin, False) 
	G.output(runningPin, True)

	os.system("python /home/pi/dingdong.py")

	G.output(statusPin, False)
	G.output(runningPin, True)

	time.sleep(10)
