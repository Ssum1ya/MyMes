from flask import Flask, request
import mysql.connector

import database_config as cfg

my_db = mysql.connector.connect(
    host = cfg.HOST,
    user = cfg.USER,
    auth_plugin = cfg.AUTH_PLAGIN,
    passwd = cfg.PASSWORD,
    database = cfg.DATABASE
)
my_cursor = my_db.cursor()
insert_reg = 'INSERT INTO users (id, login, password) VALUES (%s, %s, %s)'
insert_chat = 'INSERT INTO chats (login, chat) VALUES (%s, %s)'
select_last_id =  'SELECT id FROM users ORDER BY id DESC LIMIT 1'
check_login_for_registration = 'SELECT login FROM users WHERE login = %s;'
check_login_password = 'SELECT login, password FROM users WHERE login = %s AND password = %s;'
select_chats = 'SELECT chat FROM chats WHERE login = %s;'
select_message_lastId =  'SELECT messageId FROM messages ORDER BY messageId DESC LIMIT 1'
insert_message = 'INSERT INTO messages (messageId, login1, login2, text) VALUES (%s, %s, %s, %s)'
select_history = 'SELECT login1, text FROM messages WHERE (login1 = %s AND login2 = %s) OR (login1 = %s AND login2 = %s) ORDER BY messageId ASC'
insert_new_message = 'INSERT INTO new_messages (id, login1, login2) VALUES (%s, %s, %s)'
delete_new_message = 'DELETE FROM new_messages WHERE login1 = %s AND login2 = %s;' # SET SQL_SAFE_UPDATES = 0;
select_new_message_id = 'SELECT id FROM new_messages where login1 = %s AND login2 = %s ORDER BY id ASC'
select_new_message = 'SELECT login1, text FROM messages WHERE messageId = %s'

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
        return 'no request'

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
        return 'no request'

@app.route('/add_person2chats', methods = ['GET', 'POST'])
def add_perwon2chats():
    if request.method == 'POST':
        responce = request.get_json()

        if responce['chat'] == '':
            return 'Denied empty string'
        
        my_cursor.execute(select_chats, (responce['login'],))
        chats = my_cursor.fetchall()
        chats_array = []
        for i in range(len(chats)):
            chats_array.append(chats[i][0])
        if responce['chat'] in chats_array:
            return 'Denied already in chats'

        my_cursor.execute(check_login_for_registration, (responce['chat'],)) 
        login_coincidences = my_cursor.fetchall()
        if responce['login'] == responce['chat']:
            return 'Denied login equals chat'
        elif len(login_coincidences) != 0:
             insert_data = (responce['login'],  responce['chat'])
             my_cursor.execute(insert_chat, insert_data)
             insert_data = (responce['chat'],  responce['login'])
             my_cursor.execute(insert_chat, insert_data)
             my_db.commit()
        else:
            return 'Denied'
        return 'Success'
    else:
        return 'no request'

@app.route('/users', methods = ['GET', 'POST'])
def get_users():
    if request.method == 'POST':
        responce = request.get_json()
        
        my_cursor.execute(select_chats, (responce['login'],))
        chats = my_cursor.fetchall()
        chats_array = []
        for i in range(len(chats)):
            chats_array.append(chats[i][0])
        return chats_array
    else:
        return 'no request'

@app.route('/get_new_messages', methods = ['GET', 'POST'])
def get_new_messages():
    if request.method == 'POST':
        responce = request.get_json()

        my_cursor.execute(select_new_message_id, (responce['login1'], responce['login2'],))
        new_ids = my_cursor.fetchall()
        new_ids_array = []
        for i in range(len(new_ids)):
            new_ids_array.append(new_ids[i][0])
        
        new_messages_array = []
        for i in range(len(new_ids_array)):
            my_cursor.execute(select_new_message, (new_ids_array[i]))
        pass
    else:
        pass

@app.route('/get_history', methods = ['GET', 'POST'])
def get_history():
    if request.method == 'POST':
        responce = request.get_json()
        
        print(responce['login1'], responce['login2'])
        my_cursor.execute(delete_new_message, (responce['login2'], responce['login1'])) # multi = True
        my_db.commit()

        my_cursor.execute(select_history, (responce['login1'], responce['login2'], responce['login2'], responce['login1'],))
        messages = my_cursor.fetchall()
        messages_array = []
        for i in range(len(messages)):
            tmp_array = []
            tmp_array.append(messages[i][0])
            tmp_array.append(messages[i][1])
            messages_array.append(tmp_array)
        return messages_array
    else:
        return 'no request'

@app.route('/send_message', methods = ['GET', 'POST'])
def send_message():
    if request.method == 'POST':
        responce = request.get_json()

        my_cursor.execute(select_message_lastId)
        last_id = my_cursor.fetchone()
        message = (last_id[0] + 1, responce['login1'],  responce['login2'], responce['text'])
        new_message = (last_id[0] + 1, responce['login1'], responce['login2'])
        my_cursor.execute(insert_message, message)
        my_cursor.execute(insert_new_message, new_message)
        my_db.commit()
        return 'Success'
    else:
        return 'no request'

if __name__ == '__main__':
    app.run(debug = True)