#!/bin/bash

function initAutoanswer {
	linphonecsh init
	sleep 2
	linphonecsh register --host asterisk.ctmlabs.io --username pi --password Jr49xLMr	
	linphonecsh soundcard capture 2
	linphonecsh soundcard playback 0
	linphonecsh soundcard ring 0
	linphonecsh generic "autoanswer enable"
}

if [ ! "$(pidof linphonec)" ]; then
	initAutoanswer
else
	linphonecsh 'exit'
	initAutoanswer
fi
