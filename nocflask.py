from flask import Flask, render_template
import mysql.connector, os
# from connection import DBConnection
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
  r = db.getUrlList('SELECT * FROM endpoints')
  print(r)
  return render_template('dashboard.html', urls=r)