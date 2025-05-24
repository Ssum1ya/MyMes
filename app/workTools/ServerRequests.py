from tkinter import messagebox
import requests
import json

class ServerRequests:
    def __init__(self, main_menu, add_person2chats, registration, login):
        self.main_menu = main_menu
        self.add_person2chats = add_person2chats
        self.registration = registration
        self.login = login
    
    def log(self, user_login, user_password, login_password_id__array):
        request = requests.get('http://127.0.0.1:5000/login', json = {'login': user_login,
                                                            'password': user_password})
        server_answer = json.loads(request.content.decode())
        answer = server_answer['answer']
        if answer == 'Success':
            if len(login_password_id__array) >= 2:
                for i in range(len(login_password_id__array)):
                    login_password_id__array.pop(0)
            login_password_id__array.append(user_login)
            login_password_id__array.append(user_password)
            self.main_menu()
        elif answer == 'Denied':
            messagebox.showinfo('Ошибка', 'Не удалось найти совпадения')
            self.login()