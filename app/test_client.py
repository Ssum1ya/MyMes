import requests
import json

r = requests.get('http://127.0.0.1:5000/login')
file_name = r.headers['Content-Disposition'].split('=')[1]
file_data = r.content

with open('C:/Users/Proger/Downloads/' + file_name, 'wb') as file:
    file.write(file_data)