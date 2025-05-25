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

search_select = 'SELECT login FROM users WHERE login LIKE %s'

string = '%' + 's' + '%'

db = get_db_connection()
cursor = db.cursor()

cursor.execute(search_select, (string,))
server_login_array = cursor.fetchall()
login_array = []
for i in range(len(server_login_array)):
    login_array.append(server_login_array[i][0])


print(login_array)