from flask import Flask, render_template, request, jsonify, json, redirect
from flask_cors import CORS
import mysql.connector, os
import connection
import time
import requests
from requests.exceptions import ConnectionError
from dotenv import load_dotenv

import urllib.request
from flask import request

load_dotenv()

#################
# instantiate app
app = Flask(__name__)
app.config.from_object(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})
db = connection.DBConnection()

###############
# API Endpoints
@app.route('/ping')
def pong():
  return jsonify('pong')

@app.route('/')
def index():
  return 'Flask app running'

# return list of current api's
@app.route('/dashboard')
def dashboard():
  results = db.getUrlList('SELECT * FROM endpoints WHERE urlEnabled = 1')
  return jsonify(results)

@app.route('/create', methods=['GET','POST'])
def create():
  if request.method == 'POST':
    for item in request.json['data']['params']:
      print(item['url'])
    return 'you request the post method'
    
  if request.method == 'GET':
    return 'get method'
  
  # return redirect('/add/', 302)

@app.route('/update/<id>', methods=['GET', 'POST'])
def update(id):
  if(request.method == 'GET'):
    results = db.getById(id)
    return jsonify(results)
    # return render_template('update.html', u=results)
  
  if(request.method == 'POST'):
    return "return method is post"

@app.route('/check/', methods=['GET', 'POST']) 
def check():
  url = request.args.get('param')
  try:
    x = requests.get(url)
    print("PRINTING STATUS CODE:")
    print(x.status_code)

    if x.status_code == 200:
      start = time.time()
      y = requests.get(url)
      end = time.time()
      calltime = end - start
      envelope = {
        "url" : url,
        "statuscode" : y.status_code,
        "calltime" : calltime,
        "text" : {}
      }
      return envelope
    elif x.status_code > 215:
      print("HTTP ERROR CODE:"+ str(x.status_code))
      err215 = {
        "url" : url,
        "statuscode" : x.status_code,
        "text" : "Please check the url"
      }
      return err215
    
  ## Not needed but keeping these 
  ## error exceptions for now
  except(urllib.error.URLError):
    print( "FAILED RESULTS ARE: ")
    error1 = {
      "url" : url,
      "statuscode" : 404,
      "text" : "THE WEBSITE DOES NOT EXIST"
    }
    return error1

  except ConnectionError:
    print("UNABLE TO CONNECT TO SITE")
    error2 = {
      "url" : url,
      "statuscode" : 404,
      "text" : "UNABLE TO CONNECT TO SITE"
    }
    return error2

  except requests.RequestException:
    print("Ambigous request, try again")
    error3 = {
      "url" : url,
      "statuscode" : 404,
      "text" : "Ambigous request, try again"
    }
    return error3

  except requests.URLRequired:
    print("A VALID URL IS REQUIRED")
    error4 = {
      "url" : url,
      "statuscode" : 404,
      "text" : "A VALID URL IS REQUIRED"
    }
    return error3

  except requests.Timeout:
    print("CONNECTION TO ENDPOINT OR URL TIMED OUT")
    error5 = {
      "url" : url,
      "statuscode" : 404,
      "text" : "CONNECTION TO ENDPOINT OR URL TIMED OUT"
    }
    return error5
  
  except:
    print("throw exception")
    error6 = {
      "url" : url,
      "statuscode" : 404,
      "text" : "UNEXPECTED EXCEPTION, SORRY CHARLIE"
    }
    return error6


if __name__ == '__main__':
  app.run()

