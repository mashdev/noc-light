from flask import Flask, render_template, request
import mysql.connector, os
import connection
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
db = connection.DBConnection()

@app.route('/')
def index():
  return 'Flask app running'


@app.route('/dashboard')
def dashboard():
  r = db.getUrlList('SELECT * FROM endpoints WHERE urlEnabled = 1')
  return render_template('dashboard.html', urls=r)


@app.route('/update/<id>', methods=['GET', 'POST'])
def update(id):
  if(request.method == 'GET'):
    r = db.getById(id)
    return render_template('update.html', u=r)
  
  if(request.method == 'POST'):
    return "return method is post"
