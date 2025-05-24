from flask import Flask, request
import mysql.connector

import databaseTools.database_config as cfg

def get_db_connection():
    return mysql.connector.connect(
        host = cfg.HOST,
        user = cfg.USER,
        auth_plugin = cfg.AUTH_PLAGIN,
        passwd = cfg.PASSWORD,
        database = cfg.DATABASE
    )

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

def get_db_connection():
    return mysql.connector.connect(
        host = cfg.HOST,
        user = cfg.USER,
        auth_plugin = cfg.AUTH_PLAGIN,
        passwd = cfg.PASSWORD,
        database = cfg.DATABASE
    )

@app.route('/login', methods = ['GET'])
def login():
    if request.method == 'GET':
        responce = request.get_json()
        db = get_db_connection()
        cursor = db.cursor()

        cursor.execute(check_login_password, (responce['login'], responce['password'],))
        user_coincidences = cursor.fetchall()

        cursor.close()
        db.close()

        if len(user_coincidences) == 0:
            return {'answer' : 'Denied'}
        else:  
            return {'answer' : 'Success'}

@app.route('/registration', methods = ['POST'])
def registration():
    if request.method == 'POST':
        responce = request.get_json()
        db = get_db_connection()
        cursor = db.cursor()

        try:
            cursor.execute(check_login_for_registration, (responce['login'],)) 
            login_coincidences = cursor.fetchall()
            if len(login_coincidences) != 0:
                return {'answer' : 'Denied'} 
            else:
                cursor.execute(select_last_id)
                last_id = cursor.fetchone()
                user = (last_id[0] + 1, responce['login'],  responce['password'])
                try:
                    cursor.execute(insert_reg, user)
                except:
                    return {'answer' : 'Denied long login'}
                db.commit()
        finally:
            cursor.close()
            db.close()
        return {'answer' : 'Success'}

@app.route('/add_person2chats', methods = ['POST'])
def add_person2chats():
    if request.method == 'POST':
        responce = request.get_json()
        if responce['chat'] == '':
            return {'answer' : 'Denied empty string'}
        if responce['login'] == responce['chat']:
            return {'answer' : 'Denied login equals chat'}
        
        db = get_db_connection()
        cursor = db.cursor()

        try:
            cursor.execute(select_chats, (responce['login'],))
            chats = cursor.fetchall()
            chats_array = []
            for i in range(len(chats)):
                chats_array.append(chats[i][0])
            if responce['chat'] in chats_array:
                return {'answer' : 'Denied already in chats'}

            cursor.execute(check_login_for_registration, (responce['chat'],)) 
            login_coincidences = cursor.fetchall()
            if len(login_coincidences) != 0:
                insert_data = (responce['login'],  responce['chat'])
                cursor.execute(insert_chat, insert_data)

                insert_data = (responce['chat'],  responce['login'])
                cursor.execute(insert_chat, insert_data)

                db.commit()
            else:
                return {'answer' : 'Denied'}
        finally:
            cursor.close()
            db.close()
        return {'answer' : 'Success'}

@app.route('/users', methods = ['GET'])
def get_users():
    if request.method == 'GET':
        responce = request.get_json()
        db = get_db_connection()
        cursor = db.cursor()
        
        cursor.execute(select_chats, (responce['login'],))
        chats = cursor.fetchall()

        chats_array = []
        for i in range(len(chats)):
            cursor.execute(select_new_message_id, (chats[i][0], responce['login'],))
            new_ids = cursor.fetchall()
            
            if len(new_ids) == 0: chats_array.append([chats[i][0], 0])
            else: chats_array.append([chats[i][0], 1])

        cursor.close()
        db.close()
        return {'data' : chats_array}

@app.route('/get_new_messages', methods = ['POST'])
def get_new_messages():
    if request.method == 'POST':
        responce = request.get_json()
        db = get_db_connection()
        cursor = db.cursor()

        cursor.execute(select_new_message_id, (responce['login1'], responce['login2'],))
        new_ids = cursor.fetchall()
        new_ids_array = []
        for i in range(len(new_ids)):
            new_ids_array.append(new_ids[i][0])

        new_messages_array = []
        for i in range(len(new_ids_array)):
            cursor.execute(select_new_message, (new_ids_array[i],))
            login1_text = cursor.fetchall()
            new_messages_array.append([login1_text[0][0], login1_text[0][1]])

        cursor.execute(delete_new_message, (responce['login1'], responce['login2'])) # multi = True
        db.commit()
        
        cursor.close()
        db.close()
        return {'data' : new_messages_array}

@app.route('/get_history', methods = ['POST'])
def get_history():
    if request.method == 'POST':
        responce = request.get_json()
        db = get_db_connection()
        cursor = db.cursor()
        
        cursor.execute(delete_new_message, (responce['login2'], responce['login1'])) # multi = True
        db.commit()

        cursor.execute(select_history, (responce['login1'], responce['login2'], responce['login2'], responce['login1'],))
        messages = cursor.fetchall()
        messages_array = []
        for i in range(len(messages)):
            tmp_array = []
            tmp_array.append(messages[i][0])
            tmp_array.append(messages[i][1])
            messages_array.append(tmp_array)

        cursor.close()
        db.close()
        return {'data' : messages_array}

@app.route('/send_message', methods = ['POST'])
def send_message():
    if request.method == 'POST':
        responce = request.get_json()

        if len(responce['text']) > 253:
            return {'answer' : 'Denied long message'}
        
        db = get_db_connection()
        cursor = db.cursor()

        cursor.execute(select_message_lastId)
        last_id = cursor.fetchone()

        message = (last_id[0] + 1, responce['login1'],  responce['login2'], responce['text'])
        new_message = (last_id[0] + 1, responce['login1'], responce['login2'])

        cursor.execute(insert_message, message)
        cursor.execute(insert_new_message, new_message)

        db.commit()
        cursor.close()
        db.close()
        return {'answer' : 'Success'}

if __name__ == '__main__':
    app.run(debug = True)