import time
import datetime
import urllib3
import sys
import requests

LongestApplicationTime = 0.0
LongestApplicationURL = ""
ApplicationYellowThreshold = 2
ApplicationRedThreshold = 4
ApplicationTimeout = 6

# #General Options
# Green = 8
# Yellow = 9
# Red = 10
# Strobe = 7

# # Reverse logic here because a ground for the relay activates it
# On = False
# Off = True

# def Light(pin, status):
#   GPIO.output(pin,status)


# def console(message):
#   print("%s : %s" % (datetime.datetime.now(), message))

# apptimeout = 2
# running = True

# Array = ["test1", "test2", "test3"]
# SummaryOfPoll = []

def checkApplicationLatency(a):
  LongestApplicationTime = 0 
  try:
    # start = time.time()  
    timeToCall = requests.get(a, timeout=ApplicationTimeout).elapsed.total_seconds()
    
    # if timeToCall < 0.009:
    #   print(a, " is the fastest url", timeToCall)
    
    # if timeToCall > 0.110000:
    #   print(a, " is the slowest url", timeToCall)
    print(timeToCall, " :", a)
    # end = time.time()
    # timeToCall = end - start
    # print(timeToCall)
    #debug(i + " took " + str(timeToCall) + " seconds")
    
    # if timeToCall > LongestApplicationTime:
    #   #debug(i + " is the new slowest responding URL")
    #   LongestApplicationTime = timeToCall
    #   LongestApplicationURL = a
  except:
    print(a," failed to load request")
    # console(a)
    # console(sys.exc_info()[1])
    # SummaryOfPoll.append(a)
    # SummaryOfPoll.append(str('%.2f' % timeToCall))
    # return False
    
  return True


def MonitorUrls(urls):
    for url in urls:
      # print(url)
      checkApplicationLatency(url)
    # time.sleep(1)
    # return

# MonitorUrls(allUrls)