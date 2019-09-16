import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv(verbose=True)

class DBConnection(object):

  def __init__(self):
    self._conn = mysql.connector.connect(
      host=os.getenv('host'),
      user=os.getenv('user'),
      passwd=os.getenv('passwd'),
      database=os.getenv('database')
    )
    self._cursor = self._conn.cursor(named_tuple=True)

  def __enter__(self):
      return self

  def __exit__(self, exc_type, exc_val, exc_tb):
      self.commit()
      self.connection.close()

  @property
  def connection(self):
      return self._conn

  @property
  def cursor(self):
      return self._cursor

  def commit(self):
      self.connection.commit()

  def execute(self, sql, params=None):
      self.cursor.execute(sql, params or ())

  def fetchall(self):
      return self.cursor.fetchall()

  def fetchone(self):
      return self.cursor.fetchone()

  def query(self, sql, params=None):
      self.cursor.execute(sql, params or ())
      return self.fetchall()

  def getUrlList(self, sql):
    return self.query(sql)

  def getById(self, id):
    sql = "SELECT * FROM endpoints where id = %s"
    return self.query(sql, (id,))
  
  def insertUrlEndpoint(self, urls):
    sql = "INSERT INTO endpoints (id, urlEndpoint, urlType, UrlEnabled) VALUES (%s, %s, %s, %s) "