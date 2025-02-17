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
select_id =  "SELECT id FROM users ORDER BY id DESC LIMIT 1"
select_login = "SELECT login FROM users WHERE login = %s;"


app = Flask("server")
history = []
test_reg = []

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        history.append(request.get_json())
        print(request.get_json())
        return request.get_json()
    else:
        try:
            return history[-1]
        except:
            return "no request"

@app.route('/registration', methods = ['GET', 'POST'])
def registration():
    if request.method == 'POST':
        responce = request.get_json()
        my_cursor.execute(select_id)
        id_result = my_cursor.fetchone()
        person = (id_result[0] + 1, responce['login'],  responce['password'])
        my_cursor.execute(insert_reg, person)
        my_db.commit()
        return request.get_json()
    else:
        try:
            return test_reg[-1]
        except:
            return "no request"

if __name__ == '__main__':
    app.run(debug = True)