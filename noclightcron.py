import noclightmonitor
import mysql.connector

import time
import socket
import ssl
#import paho.mqtt.client as paho

import os
import datetime
import time
import urllib
#import urllib2
import base64
import json
import traceback
#import RPi.GPIO as GPIO
#from lxml import html
#from ntlm import HTTPNtlmAuthHandler

###########################
# NOTE: use python -m pip install mysql-connector
# to install mysql connector

#NOC Light Color Options
Green = 8
Yellow = 9
Red = 10
Strobe = 7

DEBUG = False

LoopSleep = 7
# Reverse logic here because a ground for the relay activates it
On = False
Off = True


# def Light(pin, status):
#   	GPIO.output(pin,status)


######
# Database Connection
sqldb = mysql.connector.connect(
  host="localhost",
  user="plopez",
  passwd="Gibson95!",
  database="noclightaz"
)

geturls = sqldb.cursor(named_tuple=True)
geturls.execute("SELECT urlEndpoint FROM endpoints")
results = geturls.fetchall()
scanUrl = []

for result in results:
  scanUrl.append(result.urlEndpoint)

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
realmCounter = MinRealm
apptimeout = 5
check = True

while (realmCounter <= MaxRealm):
  for s in ApplicationCheckBase:
    ApplicationCheckURLs.append(("%s%s" % (UrlBase, s)).replace('{x}', "{:0>2d}".format(realmCounter)))
  realmCounter += 1
# debug(ApplicationCheckURLs)


# postMsg = "NOC Light restarted, URLs built, polling started"
# console(postMsg)
# rpiStartupPost(postMsg)


while check:
  print("In py1")
  start = time.time()
  noclightmonitor.MonitorUrls(scanUrl)
  end = time.time()
  print(end - start)

  time.sleep(LoopSleep)

