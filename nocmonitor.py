#!/usr/bin/env python
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

LoopSleep = 5
# Reverse logic here because a ground for the relay activates it
On = False
Off = True

#Internet monitor options
TestURLList = ["http://www.google.com","http://www.yahoo.com","http://www.twitter.com"]
TestURLTimeout = 5
ApplicationCheckURLs = ["http://learn.education2020.com/educator/monitor.aspx",
"https://learn.education2020.com/educator/monitor.aspx",
"https://learn.education2020.com/contentviewers/monitor",
#"http://edgenuity.zendesk.com",
"http://auth.edgenuity.com/login/login/student",
"http://auth.edgenuity.com/login/login/educator",
"https://edgenuity.slack.com",
"http://core.learn.edgenuity.com/platformsynthesizer/EdgeStatus/FullStatus",
"http://cp.edgenuity.com/Contentplatform/api/EdgeStatus/FullStatus", 
"http://auth.edgenuity.com/Login/EdgeStatus/FullStatus",
"http://auth.edgenuity.com/AuthenticationAPI/req/EdgeStatus/FullStatus",
"http://tools.core.learn.edgenuity.com/businessapi/api/EdgeStatus/FullStatus"]
ApplicationTimeout = 6

UrlBase = "http://r{x}.core.learn.edgenuity.com/"
ApplicationCheckBase = ["ContentViewers/EdgeStatus/FullStatus", "QuestionAPI/api/EdgeStatus/FullStatus", "ContentEngineAPI/api/EdgeStatus/FullStatus", "student/EdgeStatus/FullStatus", "Educator/EdgeStatus/FullStatus", "Family/EdgeStatus/FullStatus", "LMSAPI/req/EdgeStatus/FullStatus", "Player/EdgeStatus/FullStatus"]
MinRealm = 2
MaxRealm = 22

LongestApplicationTime = 0.0
LongestApplicationURL = ""
ApplicationYellowThreshold = 2
ApplicationRedThreshold = 4

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
	time.sleep(1)
	Light(Green,Off)
	Light(Yellow,On)
	time.sleep(1)
	Light(Yellow,Off)
	Light(Red,On)
	time.sleep(1)
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

	console("POST complete, URLs to check built, beginning polling")
	while True:
		connectionWorksVal = connectionWorks()
		applicationWorksVal = applicationWorks()

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
			Light(Strobe,On)
	
		time.sleep(LoopSleep)

def debug(message):
	if(DEBUG):
		console(message)

def console(message):
	print("%s : %s" % (datetime.datetime.now(), message))
		
def applicationWorks():
	LongestApplicationTime = 0
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
			return False
			#pass

	return True

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
