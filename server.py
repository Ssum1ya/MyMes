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
insert_chat = "INSERT INTO chats (login, chat) VALUES (%s, %s)"
select_last_id =  "SELECT id FROM users ORDER BY id DESC LIMIT 1"
check_login_for_registration = "SELECT login FROM users WHERE login = %s;"
check_login_password = "SELECT login, password FROM users WHERE login = %s AND password = %s;"
select_chats = "SELECT chat FROM chats WHERE login = %s;"

app = Flask("server")

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        responce = request.get_json()
        my_cursor.execute(check_login_password, (responce['login'], responce['password'],))
        user_coincidences = my_cursor.fetchall()
        if len(user_coincidences) == 0:
            return 'Denied'
        else:  
            return 'Success'
    else:
        return "no request"

@app.route('/registration', methods = ['GET', 'POST'])
def registration():
    if request.method == 'POST':
        responce = request.get_json()
        my_cursor.execute(select_last_id)
        last_id = my_cursor.fetchone()

        my_cursor.execute(check_login_for_registration, (responce['login'],)) 
        login_coincidences = my_cursor.fetchall()
        if len(login_coincidences) != 0:
            return 'Denied' 
        else:
            user = (last_id[0] + 1, responce['login'],  responce['password'])
            try:
                my_cursor.execute(insert_reg, user)
            except:
                return 'Denied long login'
            my_db.commit()
        return 'Success'
    else:
        return "no request"

@app.route('/add_person2chats', methods = ['GET', 'POST'])
def add_perwon2chats():
    if request.method == 'POST':
        responce = request.get_json()
        my_cursor.execute(check_login_for_registration, (responce['login'],)) 
        login_coincidences = my_cursor.fetchall()
        if responce['login'] == responce['chat']:
            return 'Denied login equals chat'
        elif len(login_coincidences) != 0:
             insert_data = (responce['login'],  responce['chat'])
             my_cursor.execute(insert_chat, insert_data)
             my_db.commit()
        else:
            return 'Denied'
        return 'Success'
    else:
        pass

@app.route('/users', methods = ['GET', 'POST'])
def get_users():
    if request.method == 'POST':
        responce = request.get_json()
        my_cursor.execute(select_chats, (responce['login'],))
        chats = my_cursor.fetchall()
        chats_array = []
        for i in range(len(chats)):
            chats_array.append(chats[i][0])
        print(chats_array)
        return chats_array
    else:
        pass

@app.route('/get_new_messages', methods = ['GET', 'POST'])
def get_new_messages():
    if request.method == 'POST':
        pass
    else:
        pass

@app.route('/get_history', methods = ['GET', 'POST'])
def get_history():
    if request.method == 'POST':
        pass
    else:
        pass

@app.route('/send_message', methods = ['GET', 'POST'])
def send_message():
    if request.method == 'POST':
        pass
    else:
        pass

if __name__ == '__main__':
    app.run(debug = True)