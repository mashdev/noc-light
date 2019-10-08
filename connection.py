import mysql.connector
import os, json
from flask import redirect, render_template, url_for, jsonify
from dotenv import load_dotenv

load_dotenv(verbose=True)

class DBConnection(object):

  host = os.getenv('host'),
  user = os.getenv('user'),
  pw = os.getenv('passwd'),
  db = os.getenv('database')

  def __init__(self, host = os.getenv('host'), user = os.getenv('user'), pw = os.getenv('passwd'), db = os.getenv('database')):
    self.conn = mysql.connector.connect(
      host = host,
      user = user,
      passwd=pw,
      database=db
    )
  
  def reset(self):
    self.conn.reset_session()


  def getUrlList(self, query):
    c = self.conn.cursor()
    c.execute(query)
    results = c.fetchall()
    self.reset()
    return results

  def getById(self, id):
    c = self.conn.cursor(dictionary=True)
    c.execute("SELECT * FROM endpoints e INNER JOIN urlcategories u ON u.catid = e.urlType WHERE id = %s", (id,) )
    result = c.fetchall()
    self.reset()
    return result, self.getCategoryList()


  def getByEndpointName(self, names):
    name = names.rstrip('/')
    c = self.conn.cursor()
    c.execute("SELECT COUNT(*) urlEndpoint FROM endpoints WHERE urlEndpoint = %s", (name,))
    result = c.fetchone()
    self.reset()
    return result

  def getCategoryList(self):
    c = self.conn.cursor(dictionary=True)
    c.execute("SELECT * FROM urlcategories")
    result = c.fetchall()
    # self.reset()
    return result

  def insertUrlEndpoint(self, url):
    urls = url.rstrip('/')
    try:
      query = self.getByEndpointName(urls)
      checkDupe = query[0]
      print(checkDupe)
      
      if checkDupe == 0:
        print("Inside checkDupe function")
        c = self.conn.cursor()
        c.execute('INSERT INTO endpoints (urlEndpoint, urlType, urlEnabled) VALUES (%s,1,1)', (urls,) )
        rc = c.rowcount
        print(rc)

        if rc == 1:
          self.conn.commit()
          result = {
            'stat': 200,
            'reason': 'Endpoint saved to database',
            'url': str(urls)
          }
          return result

        elif rc == 0:
          return "Entry was not committed to database"

      if checkDupe == 1:
        print("Url already exists in the system")
        dupe = {
          'stat': 800,
          'reason': 'Url already in database',
          'url': str(urls)
        }
      return dupe

    except mysql.connector.Error as e:
      print ("Error:%d:%s" % (e.args[0], e.args[1]))
    

  def updateUrlEndpoint(self, obj):
    row = json.loads(obj)
    endpoint = row['body']['endpoint']
    urltype = row['body']['urltype']
    isenabled = row['body']['isenabled']
    uid = row['body']['uid']

    try:
      c = self.conn.cursor()
      c.execute('Update endpoints SET urlEndpoint=%s, urlType=%s, urlEnabled=%s WHERE id=%s', (endpoint, urltype, isenabled, uid,))
      rc = c.rowcount

      if rc >= 1:
        self.conn.commit()
        return json.dumps({'success':'201'}), 200, {'ContentType':'application/json'}
    
    except NameError:
      return json.dumps({'failed': 404}), 404, {'ContentType':'application/json'}