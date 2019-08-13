#!/usr/bin/env python
import socket
import ssl
import paho.mqtt.client as paho
import sys
import os
import datetime
import time
import urllib
import urllib2
import base64
import json
import traceback
import RPi.GPIO as GPIO
from lxml import html
from ntlm import HTTPNtlmAuthHandler

#General Options
Green = 8
Yellow = 9
Red = 10
Strobe = 7

DEBUG = False

LoopSleep = 7
# Reverse logic here because a ground for the relay activates it
On = False
Off = True

#Internet monitor options
TestURLList = ["http://www.google.com","http://www.yahoo.com","http://www.twitter.com"]
TestURLTimeout = 5
ApplicationCheckURLs = ["http://learn.education2020.com/educator/monitor.aspx",
"https://learn.education2020.com/educator/monitor.aspx",
"https://learn.education2020.com/contentviewers/monitor",
"http://auth.edgenuity.com/login/login/student",
"http://auth.edgenuity.com/login/login/educator",
"https://edgenuity.slack.com",
"http://core.learn.edgenuity.com/platformsynthesizer/EdgeStatus/FullStatus",
"http://cp.edgenuity.com/Contentplatform/api/EdgeStatus/FullStatus", 
"http://auth.edgenuity.com/Login/EdgeStatus/FullStatus",
"http://auth.edgenuity.com/AuthenticationAPI/req/EdgeStatus/FullStatus",
"http://tools.core.learn.edgenuity.com/businessapi/api/EdgeStatus/FullStatus"]

ApplicationTimeout = 6
## Setting below for testing purposes
#ApplicationTimeout = .2

UrlBase = "http://r{x}.core.learn.edgenuity.com/"
ApplicationCheckBase = ["ContentViewers/EdgeStatus/FullStatus", "QuestionAPI/api/EdgeStatus/FullStatus", "ContentEngineAPI/api/EdgeStatus/FullStatus", "student/EdgeStatus/FullStatus", "Educator/EdgeStatus/FullStatus", "Family/EdgeStatus/FullStatus", "LMSAPI/req/EdgeStatus/FullStatus", "Player/EdgeStatus/FullStatus"]
MinRealm = 2
MaxRealm = 22

LongestApplicationTime = 0.0
LongestApplicationURL = ""
ApplicationYellowThreshold = 2
ApplicationRedThreshold = 4

## Start AWS Settings ##
connflag = True

# function for making connection to AWS
def on_connect(client, userdata, flags, rc):
	global connflag
	print("Connected to AWS")
	connflag = True
	print("Connection returned result: " + str(rc) )

 
# Function for Sending msg payload
def on_message(client, userdata, msg):
	print(msg.topic+" "+str(msg.payload))


## for logging purposes
def on_log(client, userdata, level, buf):
	print(msg.topic+" "+str(msg.payload))



# mqttc object
mqttc = paho.Client()
# assign on_connect func
mqttc.on_connect = on_connect
# assign on_message function
mqttc.on_message = on_message
mqttc.on_log = on_log

#### Change following parameters #### 
# Noc-Light-Scottsdale AWS endpoint
awshost = "a1buulfaeqxah3-ats.iot.us-east-1.amazonaws.com"
# Default AWS port for IoT
awsport = 8883
# Thing_Name
clientId = "Noc-Light-Scottsdale"
# Thing_Name
thingName = "Noc-Light-Scottsdale"
# Root_CA_Certificate_Name
caPath = "root-CA.crt"
# <Thing_Name>.cert.pem
certPath = "Noc-Light-Scottsdale.cert.pem"
# <Thing_Name>.private.key
keyPath = "Noc-Light-Scottsdale.private.key"
# pass parameters to mqttc
mqttc.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)
# connect to aws server
mqttc.connect(awshost, awsport, keepalive=60)

## End AWS Settings ##

#to play a sound do it as follows:
#os.system('mpg321 SadTrombone.mp3 &')


def main():
	console("Starting script, Beginning POST")
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(Green,GPIO.OUT)
	GPIO.setup(Yellow,GPIO.OUT)
	GPIO.setup(Red,GPIO.OUT)
	GPIO.setup(Strobe,GPIO.OUT)

	Light(Green,On)
	time.sleep(.5)
	Light(Green,Off)
	Light(Yellow,On)
	time.sleep(.5)
	Light(Yellow,Off)
	Light(Red,On)
	time.sleep(.5)
	Light(Red,Off)
	Light(Strobe,On)
	time.sleep(1)
	Light(Strobe,Off)

	realmCounter = MinRealm

	while (realmCounter <= MaxRealm):
		for s in ApplicationCheckBase:
			ApplicationCheckURLs.append(("%s%s" % (UrlBase, s)).replace('{x}', "{:0>2d}".format(realmCounter)))
		realmCounter += 1
	debug(ApplicationCheckURLs)

	postMsg = "NOC Light restarted, URLs built, polling started"
	console(postMsg)
	rpiStartupPost(postMsg)
	
	while True:
		connectionWorksVal = connectionWorks()
		applicationWorksVal = applicationWorks()
		awsPost = errMsgToAws("start")
    
		
		if LongestApplicationTime > ApplicationRedThreshold:
			console("Application running slowly: " + LongestApplicationURL)
			Light(Red,On)
			Light(Yellow,Off)
			Light(Green,Off)
		elif LongestApplicationTime > ApplicationYellowThreshold:
			console("Application beginning to get sluggish: " + LongestApplicationURL)
			Light(Red,Off)
			Light(Yellow,On)
			Light(Green,Off)
		else:
			debug("everything ok")
			Light(Red,Off)
			Light(Yellow,Off)
			Light(Green,On)
			
		if connectionWorksVal and applicationWorksVal:
			Light(Strobe,Off)
		else:
			if not connectionWorksVal:
				console("Can't verify connection to internet")
			if not applicationWorksVal:
				console("Application down or system slowness")
				SummaryOfPoll.append("Application down or system slowness")
			Light(Strobe,On)
	
		time.sleep(LoopSleep)
		
		if len(SummaryOfPoll) > 0:
			for summary in SummaryOfPoll:
				print(summary)

			errMsgToAws(SummaryOfPoll)
			del SummaryOfPoll[:]

def debug(message):
	if(DEBUG):
		console(message)


def console(message):
	print("%s : %s" % (datetime.datetime.now(), message))

SummaryOfPoll = []

def applicationWorks():
	LongestApplicationTime = 0
	global SummaryOfPoll

	for i in ApplicationCheckURLs:
		try:
			start = time.time()
			urllib2.urlopen(i,timeout=ApplicationTimeout).close()
			end = time.time()
			timeToCall = end - start
			debug(i + " took " + str(timeToCall) + " seconds")
			if timeToCall > LongestApplicationTime:
				debug(i + " is the new slowest responding URL")
				LongestApplicationTime = timeToCall
				LongestApplicationURL = i
		except:
			console(i)
			console(sys.exc_info()[1])
			SummaryOfPoll.append(i)
			SummaryOfPoll.append(str('%.2f' % timeToCall))
			return False
			#pass

	return True


## Standard triggered errors  ##
def errMsgToAws(msg):
	if msg != "start":
		colorStatus = "#F9F037"
		try:
			msgLen = len(msg)
			messageText = ""
			for m in range(msgLen):
				if len(msg[m]) <= 5:
					msg[m] = float(msg[m])
					msg[m] = msg[m] * 100

					if msg[m] <= 3.0:
						colorStatus = "#FFFF00"  #Yellow
					elif 3.1 <= msg[m] <= 3.9:
						colorStatus = "#FFA500"  #Orange
					elif msg[m] < 4.0:
						colorStatus = "#FF0000"  #Red
				messageText += str(msg[m]) + "\n"

			errMessage = {
					"attachments": [
							{
									"fallback": "NOC-Light Triggered",
									"color": colorStatus,
									"title": "Light Triggered",
									"text": messageText,
									"footer": "NOC-LIGHT",
									"footer_icon": "https://platform.slack-edge.com/img/default_application_icon.png",
									"ts": time.time()
							}
					]
			}
			# return errMessage
			mqttc.publish("noclight-scottsdale", json.dumps(errMessage), qos=1)
		except:
			print("Requested index is higher than array")

def rpiStartupPost(msg):
	colorStatus = "#008000"
	startMessage = 	{
    "attachments": [
        {
            "fallback": "NOC-Light Triggered",
            "color": colorStatus,
            "title": "Light Triggered",
						"text": msg,
            "footer": "NOC-LIGHT",
            "footer_icon": "https://platform.slack-edge.com/img/default_application_icon.png",
						"ts" : time.time()
        }
    ]
	}
	mqttc.publish("noclight-scottsdale", json.dumps(startMessage), qos=1)
	return


## Function creates a slack template with params
def displayError(url, sc, ttc, st):
	showError = 	{
						"attachments": [
								{
										"fallback": url,
										"color": "danger",
										"pretext": "Light Triggered",
										"title": url,
										"text" : str(sc) +" at "+ str('%.2f' % ttc) + " seconds",
										"footer": "NOC-LIGHT",
										"footer_icon": "https://platform.slack-edge.com/img/default_application_icon.png",
										"ts" : st
								}
						]
				}
	return showError

def connectionWorks():
	#rotate the array so we aren't always trying the same outside site
	global TestURLList
	TestURLList = rotate(TestURLList)
	
	for i in TestURLList:
		try:
			debug(i)
			urllib2.urlopen(i,timeout=TestURLTimeout).close()
			return True
		except:
			console("Connection to internet failure")
			console(i)
			console(sys.exc_info()[1])
			pass
			
	return False

def Light(pin, status):
	GPIO.output(pin,status)

def rotate(l, y=1):
   if len(l) == 0:
      return l
   y = y % len(l)    # Why? this works for negative y

   return l[y:] + l[:y]


if __name__=="__main__":
	main()
	