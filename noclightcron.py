import noclightmonitor
import mysql.connector
from dotenv import load_dotenv
import time
import socket
import ssl
#import paho.mqtt.client as paho

import os
import json
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

load_dotenv('.env')

########################
# get creds from .env file
dbhost = os.getenv('host')
dbuser = os.getenv('user')
dbpass = os.getenv('passwd')
dbdb = os.getenv('database')



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
  host = dbhost,
  user = dbuser,
  password = dbpass,
  database = dbdb
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

print("Restarting the NOC Light, don't freak out...")
# os.system('/usr/bin/supervisorctl restart noc_monitor')


while check:
  print("In py1")
  start = time.time()
  noclightmonitor.MonitorUrls(scanUrl)
  end = time.time()
  print(end - start)

  time.sleep(LoopSleep)

