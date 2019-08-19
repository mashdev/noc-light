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

#########################
#NOC Light Color Options
Green = 8
Yellow = 9
Red = 10
Strobe = 7
DEBUG = False

#####################
# Loop length seconds
LoopSleep = 7

# Reverse logic here because a ground for the relay activates it
On = False
Off = True

# def Light(pin, status):
#   	GPIO.output(pin,status)


#####################
# Database Connection
sqldb = mysql.connector.connect(
  host="localhost",
  user="plopez",
  passwd="Gibson95!",
  database="noclightaz"
)

#####################
# create sql select statement
geturls = sqldb.cursor(named_tuple=True)
geturls.execute("SELECT urlEndpoint FROM endpoints")
results = geturls.fetchall()
scanUrl = []

##########################
# put db results to array
for result in results:
  scanUrl.append(result.urlEndpoint)

#########################
#Internet monitor options
TestURLList = ["http://www.google.com","http://www.yahoo.com","http://www.twitter.com"]
TestURLTimeout = 5


# ApplicationTimeout = 6
## Setting below for testing purposes
#ApplicationTimeout = .2

apptimeout = 5
check = True

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

