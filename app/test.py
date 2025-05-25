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

string = '%' + 'Ao' + '%'

db = get_db_connection()
cursor = db.cursor()

cursor.execute(search_select, (string,))
user_coincidences = cursor.fetchall()
print(user_coincidences)