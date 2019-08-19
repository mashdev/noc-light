import time
import datetime
import urllib3
import sys
import requests

LongestApplicationTime = 0.150000
LongestApplicationURL = ""
ApplicationYellowThreshold = 2
ApplicationRedThreshold = 4
# ApplicationTimeout = 6
ApplicationTimeout = 0.26000

#################
# General Options
# Green = 8
# Yellow = 9
# Red = 10
# Strobe = 7

##################################################################
# Reverse logic here because a ground for the relay activates it
# On = False
# Off = True

# def Light(pin, status):
#   GPIO.output(pin,status)

################################
# print to Supervisor.d console
# def console(message):
#   print("%s : %s" % (datetime.datetime.now(), message))

# apptimeout = 2
# running = True

# SummaryOfPoll = []
fastestUrls = []

red = "#FE0C2F"
yellow = "#F9FE01"
green = "#42F109"

def checkApplicationLatency(a):
  try:
    # timeToCall = requests.get(a, timeout=LongestApplicationTime).elapsed.total_seconds()
    start = time.time()
    requests.get(a, stream=True).close()
    end = time.time()
    timeToCall = end - start
    # print(timeToCall)

    if timeToCall < 0.009:
      fastestUrls.append(a)
      print(a, "is the fastest")

    # if timeToCall > 0.110000:
    #   print(a, " is the slowest url", timeToCall)
    #   requests.post(
    #     webhook_url,
    #     json=slackMessage(text=a, color=red),
    #     headers={'Content-Type': 'application/json'}
    #   )
    # elif 0.10000 < timeToCall:
    #   print(a, " Fast")
    #   requests.post(
    #     webhook_url,
    #     json=slackMessage(text=a, color=green),
    #     headers={'Content-Type': 'application/json'}
    #   )
    # else:
    #   pass

    #debug(i + " took " + str(timeToCall) + " seconds")
    
    # if timeToCall > LongestApplicationTime:
    #   #debug(i + " is the new slowest responding URL")
    #   LongestApplicationTime = timeToCall
    #   LongestApplicationURL = a
  except:
    print("slowest url is:", a)
    requests.post(
      webhook_url,
      json=slackMessage(text=a, color=red),
      headers={'Content-Type': 'application/json'}
    )

    # print(a,"timed out")
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
    # return fastestUrls

webhook_url = "https://hooks.slack.com/services/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"

def slackMessage(
        fall="",
        color="#7F7F80",
        pre="",
        title="Light Trigger Test",
        text="test test test",
        footer="NOC-LIGHT"):
    showError = {
        "attachments": [
            {
                "fallback": fall,
                "color": color,
                "pretext": pre,
                "title": title,
                "text": text,
                "footer": footer,
                "footer_icon": "https://platform.slack-edge.com/img/default_application_icon.png",
                "ts": time.time()
            }
        ]
    }
    return showError



