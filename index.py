from bottle import route, run
import mysql.connector

@route('/hello/<name>')
def index(name):
    return template('<b>Hello {{name}}</b>!', name=name)

run(host='localhost', port=8080, reloader=True)