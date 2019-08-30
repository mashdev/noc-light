from flask import Flask, render_template, request, jsonify, json
from flask_cors import CORS
import mysql.connector, os
import connection
import time
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

@app.route('/ping')
def pong():
  return jsonify('pong')

@app.route('/')
def index():
  return 'Flask app running'


@app.route('/dashboard')
def dashboard():
  results = db.getUrlList('SELECT * FROM endpoints WHERE urlEnabled = 1')
  return jsonify(results)


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

  start = time.time()
  x = urllib.request.urlopen(url)
  end = time.time()
  calltime = end-start
  
  if x.status == 200:
    envelope = {
      "url" : url,
      "body" : x.status,
      "calltime" : '{0:.2g}'.format(calltime)
    }
    return envelope
  
  else:
    failed = {
      "url" : url,
      "body" : x.status,
      "calltime" : '{0:.2g}'.format(calltime)
    }

  # try:
  #   if x.status == 200:
  #     print(x.read())
  #     return x.read()
  
  # except:
  #   if x.status == 500 | x.status == 400 | x.status == 404:
  #     print("API FAILED TO RESOLVE TO URL")
  #     return

  # try:
  #   start = time.time()
  #   x = urllib.request.urlopen(url)
  #   end = time.time()
  #   total = end   - start
  #   print(end - start)

  #   envelope = {
  #     "url" : url,
  #     "body" : x.status,
  #     "calltime" : '{0:.2g}'.format(total)
  #   }
  #   return envelope

  # except:
  #   x = urllib.request.urlopen(url)
  #   if x.status == 500:
  #     print("API Url is not reachable")
  #   return


if __name__ == '__main__':
  app.run()