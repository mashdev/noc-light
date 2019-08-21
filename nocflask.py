from flask import Flask, render_template
import mysql.connector, os
from dotenv import load_dotenv
load_dotenv(verbose=True)


app = Flask(__name__)
app.secret_key = b'(*&gh8&&G*&^]4%^&D*B:*m-*Nd*76v9&^)'

sqldb = mysql.connector.connect(
  host=os.getenv('host'),
  user=os.getenv('user'),
  passwd=os.getenv('passwd'),
  database=os.getenv('database')
)

@app.route('/')
def index():
  
  return 'Flask app running'


@app.route('/dashboard')
def dashboard():
  geturls = sqldb.cursor(named_tuple=True)
  geturls.execute("SELECT urlEndpoint FROM endpoints")
  results = geturls.fetchall()

  return render_template('dashboard.html', urls=results)