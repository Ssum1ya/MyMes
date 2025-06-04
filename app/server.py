from flask import Flask, request, send_file
import mysql.connector
import base64
import os

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
search_select = 'SELECT login FROM users WHERE login LIKE %s'

server_files_path = 'C:/Users/Proger/Desktop/server_files/'
insert_file = 'INSERT INTO files (id, login1, login2, name, path) VALUES (%s, %s, %s, %s, %s)'
select_files_lastId =  'SELECT id FROM files ORDER BY id DESC LIMIT 1'
select_files = 'SELECT name FROM files WHERE (login1 = %s AND login2 = %s) OR (login1 = %s AND login2 = %s) ORDER BY id ASC'
select_path = 'SELECT path FROM files WHERE (login1 = %s AND login2 = %s) OR (login1 = %s AND login2 = %s) AND name = %s;'

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

@app.route('/searchLogin', methods = ['GET'])
def search():
    if request.method == 'GET':
        responce = request.get_json()
        db = get_db_connection()
        cursor = db.cursor()

        string_arg = '%' + responce['login_piece'] + '%'
        cursor.execute(search_select, (string_arg,))
        server_login_array = cursor.fetchall()

        login_array = []
        for i in range(len(server_login_array)):
            login_array.append(server_login_array[i][0])

        cursor.close()
        db.close()

        return {'data' : login_array}
    
@app.route('/send_files', methods = ['GET', 'POST'])
def send_files():
    if request.method == 'GET':
        responce = request.get_json()
        db = get_db_connection()
        cursor = db.cursor()

        cursor.execute(select_files, (responce['login1'], responce['login2'], responce['login2'], responce['login1'],))
        messages = cursor.fetchall()
        files_array = []
        for i in range(len(messages)):
            files_array.append(messages[i][0])
        
        cursor.close()
        db.close() 
        return {'data' : files_array}
    
    elif request.method == 'POST':
        responce = request.get_json()
        db = get_db_connection()
        cursor = db.cursor()

        name = responce['file_name']
        file_data = base64.b64decode(responce['file_data'])
        login1, login2 = responce['login1'], responce['login2']

        path = None
        path1 = server_files_path + login1 + '-' + login2
        path2 = server_files_path + login2 + '-' + login1
        if not os.path.exists(path1) and not os.path.exists(path2):
            os.mkdir(path1)
            path = path1
        elif os.path.exists(path1): path = path1
        elif os.path.exists(path2): path = path2
        
        if os.path.exists(path + '/' + name):
            return {'answer' : 'Denied'}

        with open(path + '/' + name, 'wb') as file:
            file.write(file_data)

        cursor.execute(select_files_lastId)
        id = None
        last_id = cursor.fetchone()
        if last_id == None: id = 1
        else: id = last_id[0] + 1

        add_file = (id, login1,  login2, name, path)
        cursor.execute(insert_file, add_file)

        db.commit()
        cursor.close()
        db.close()   
        return {'answer' : 'Succes'}

@app.route('/download_file', methods = ['GET'])
def download_file():
    if request.method == 'GET':
        responce = request.get_json()
        db = get_db_connection()
        cursor = db.cursor()

        cursor.execute(select_path, (responce['login1'], responce['login2'], responce['login2'], responce['login1'], responce['name']))
        path = cursor.fetchall()

        cursor.close()
        db.close()
        return send_file(path[0][0] + '/' + responce['name'], as_attachment = True, download_name = responce['name'])

if __name__ == '__main__':
    app.run(debug = True)