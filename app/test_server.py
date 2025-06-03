from flask import Flask, request, send_file
import base64
import os

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

app = Flask("server")
file_name = 'kiyotaka.jpg'
server_files_path = 'C:/Users/Proger/Desktop/server_files/'

insert_file = 'INSERT INTO files (id, login1, login2, name, path) VALUES (%s, %s, %s, %s, %s)'
select_files_lastId =  'SELECT id FROM files ORDER BY id DESC LIMIT 1'
select_files = 'SELECT name FROM files WHERE (login1 = %s AND login2 = %s) OR (login1 = %s AND login2 = %s) ORDER BY id ASC'
select_path = 'SELECT path FROM files WHERE (login1 = %s AND login2 = %s) OR (login1 = %s AND login2 = %s) AND name = %s;'

@app.route('/send_files', methods = ['GET', 'POST'])
def login():
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
        #return send_file(file_name, as_attachment = True, download_name = 'zxc.jpg')
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