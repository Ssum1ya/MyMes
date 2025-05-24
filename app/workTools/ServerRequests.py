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
    
    def reg(self, user_login, password1, password2):
        if password1 != password2:
            messagebox.showinfo('Ошибка', 'Не удалось зарегистрироваться так как пароли не совпадают')
            self.registration()
        else:
            request = requests.post('http://127.0.0.1:5000/registration', json = {'login': user_login,
                                                                            'password': password1})
            server_answer = json.loads(request.content.decode())
            answer = server_answer['answer']
            if answer == 'Success':
                messagebox.showinfo('Успешно', 'Теперь войдите под своей учетной записью')
                self.login()
            elif answer == 'Denied':
                messagebox.showinfo('Ошибка', 'Не удалось зарегистрироваться так как такой логин уже есть')
                self.registration()
            elif answer == 'Denied long login':
                messagebox.showinfo('Ошибка', 'Не удалось зарегистрироваться так как логин слишком длинный')
                self.registration()
    
    def check_login_in_bd(self, user_login, login_password_id__array):
        request = requests.post('http://127.0.0.1:5000/add_person2chats', json = {'chat': user_login,
                                                                                'login': login_password_id__array[0]})
        server_answer = json.loads(request.content.decode())
        answer = server_answer['answer']
        if answer == 'Success':
            messagebox.showinfo('Успех', 'пользователь успешно добавлен в ваши чаты')
            self.main_menu()
        elif answer == 'Denied':
            messagebox.showinfo('Ошибка', 'не удалось найти пользователя с логином')
            self.add_person2chats()
        elif answer == 'Denied login equals chat':
            messagebox.showinfo('Ошибка', 'ваш логин равен чату который хотите добавить')
            self.add_person2chats()
        elif answer == 'Denied empty string':
            messagebox.showinfo('Ошибка', 'введите не пустую строку')
            self.add_person2chats()
        elif answer == 'Denied already in chats':
            messagebox.showinfo('Ошибка', 'этот пользователь уже у вас в чатах')
            self.add_person2chats()

    def show_history_messages(self, user_chat, login_password_id__array):
        request = requests.post('http://127.0.0.1:5000/get_history', json = {'login1': login_password_id__array[0],
                                                                                        'login2': user_chat})
        server_answer = json.loads(request.content.decode())
        data = server_answer['data']

        #TODO: вынести в функцию
        login1_mas = []
        message_mas = []
        for i in range(len(data)):
            login1_mas.append(data[i][0].strip())
            message_mas.append(data[i][1].strip()) 

        return login1_mas, message_mas