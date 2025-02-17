import database_config as cfg

from flask import Flask, url_for, request
import mysql.connector

my_db = mysql.connector.connect(
    host = cfg.host,
    user = cfg.user,
    auth_plugin = cfg.auth_plugin,
    passwd = cfg.passwd,
    database = cfg.database
)
my_cursor = my_db.cursor()
insert_reg = "INSERT INTO users (id, login, password) VALUES (%s, %s, %s)"

app = Flask("server")
history = []
test_reg = []

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        history.append(request.get_json())
        return request.get_json()
    else:
        try:
            return history[-1]
        except:
            return "no request"

@app.route('/registration', methods = ['GET', 'POST'])
def registration():
    if request.method == 'POST':
        test_reg.append(request.get_json())
        return request.get_json()
    else:
        try:
            return test_reg[-1]
        except:
            return "no request"

if __name__ == '__main__':
    app.run(debug = True)