from tkinter import Tk, Label, Button, Entry, Listbox, Frame, StringVar, Scrollbar
from tkinter import RIGHT, LEFT, BOTH, Y, END
from tkinter import messagebox
import requests
from threading import Thread
from time import sleep

from ServerResponceHandler import ServerResponceHandler

root = Tk()
root.geometry('400x600')
root.title('Войти в систему')

login_password_id__array = []
thread_flag = True

def clear():
    for widget in root.winfo_children():
    	widget.destroy()

def main_menu():
    global thread_flag
    thread_flag = False
    clear()
    main_title = Label(text = 'Главное Меню')
    button_back = Button(text = 'Назад', command = choise)
    button_chats = Button(text = 'Мои чаты', command = lambda: show_my_chats())
    button_add2chats = Button(text = 'добавить человека в чат', command = lambda: add_person2chats())
    main_title.pack()
    button_add2chats.pack()
    button_chats.pack()
    button_back.pack()

def show_my_chats():
    clear()
    main_title = Label(text = 'Ваш список чатов')
    main_title.pack()

    request = requests.post('http://127.0.0.1:5000/users', json = {'login': login_password_id__array[0]})
    chats = request.content.decode()

    chats_mas, ids_mas = ServerResponceHandler.chats_handler(chats)
    for i in range(len(chats_mas)):
        if ids_mas[i] == '1':
            chat_title = Label(text = chats_mas[i], background = "#00FF00") #background = "#00FF00"
        else:
            chat_title = Label(text = chats_mas[i])
        chat_title.pack()
        
    select_title = Label(text = 'Напишите чат который хоите выбрать')
    select_title.pack()
    select_chat = Entry()
    select_chat_button = Button(text = 'Выбрать чат', command = lambda : chat(select_chat.get()))
    select_chat.pack()
    select_chat_button.pack()
    button_back = Button(text = 'Назад', command = main_menu)
    button_back.pack()

def add_person2chats():
    clear()
    main_title = Label(text = 'Введите логин того кого хотите добавить в чаты')
    person_login = Entry()
    button_check = Button(text = 'Добавить', command = lambda : check_login_in_bd(person_login.get(), ))
    button_back = Button(text = 'Назад', command = main_menu)
    main_title.pack()
    person_login.pack()
    button_check.pack()
    button_back.pack()

def check_login_in_bd(user_login):
    request = requests.post('http://127.0.0.1:5000/add_person2chats', json = {'chat': user_login,
                                                                              'login': login_password_id__array[0]})
    if request.content == b'Success':
        messagebox.showinfo('Успех', 'пользователь успешно добавлен в ваши чаты')
        main_menu()
    elif request.content == b'Denied':
        messagebox.showinfo('Ошибка', 'не удалось найти пользователя с логином')
        add_person2chats()
    elif request.content == b'Denied login equals chat':
        messagebox.showinfo('Ошибка', 'ваш логин равен чату который хотите добавить')
        add_person2chats()
    elif request.content == b'Denied empty string':
        messagebox.showinfo('Ошибка', 'введите не пустую строку')
        add_person2chats()
    elif request.content == b'Denied already in chats':
        messagebox.showinfo('Ошибка', 'этот пользователь уже у вас в чатах')
        add_person2chats()

def chat(user_chat):
    global thread_flag
    thread_flag = True
    clear()
    login1_mas, message_mas = show_history_messages(user_chat)
        
    messages_frame = Frame(root)
    my_msg = StringVar()
    my_msg.set('Введите ваше сообщение здесь.')
    scrollbar = Scrollbar(messages_frame)

    msg_list = Listbox(messages_frame, height = 15, width = 50, yscrollcommand = scrollbar.set)
    scrollbar.pack(side = RIGHT, fill = Y)
    msg_list.pack(side = LEFT, fill = BOTH)
    msg_list.pack()
    messages_frame.pack()

    button_back = Button(text = 'Назад', command = main_menu)

    entry_field = Entry(root, textvariable = my_msg)
    entry_field.bind('<Return>')
    entry_field.pack()

    send_button = Button(root, text = 'отправить', command = lambda: send_message(entry_field.get(), msg_list, user_chat))
    button_back.pack()
    send_button.pack()
    root.protocol("WM_DELETE_WINDOW")

    for i in range(len(message_mas)):
        login1 = login1_mas[i]
        message = message_mas[i]
        msg_list.insert(END, f'{login1} : {message}')

    msg_list.yview_scroll(number = len(message_mas), what = 'units')

    loading_history_thread = Thread(target = lambda: load_new_message(msg_list, user_chat))
    loading_history_thread.start()

def load_new_message(msg_list, user_chat):
    flag = True              
    while flag and thread_flag:
        sleep(5)
        request = requests.post('http://127.0.0.1:5000/get_new_messages', json = {'login1' : user_chat, 
                                                                          'login2': login_password_id__array[0]})
        messages = request.content.decode()
        login1_mas, message_mas = ServerResponceHandler.message_handler(messages)
        
        for i in range(len(message_mas)):
            login1 = login1_mas[i]
            message = message_mas[i]
            try:
                msg_list.insert(END, f'{login1} : {message}')
            except:
                flag = False
            msg_list.yview_scroll(number = 1, what = 'units')

def send_message(message, msg_list, user_chat):
    request = requests.post('http://127.0.0.1:5000/send_message', json = {'login1': login_password_id__array[0],
                                                                                     'login2': user_chat,
                                                                                     'text': message})
    msg_list.insert(END, f'{login_password_id__array[0]} : {message}')
    msg_list.yview_scroll(number = 1, what = 'units')

def show_history_messages(user_chat):
    request = requests.post('http://127.0.0.1:5000/get_history', json = {'login1': login_password_id__array[0],
                                                                                     'login2': user_chat})
    messages = request.content.decode()
    login1_mas, message_mas = ServerResponceHandler.message_handler(messages)
    
    return login1_mas, message_mas

def choise():
    clear()
    button_registr = Button(text = 'Зарегистрироваться', command = registration)
    buttion_login = Button(text = 'Войти', command = login)
    button_registr.pack()
    buttion_login.pack()

def registration():
    clear()
    main_title = Label(text = 'Для входа в систему зарегистрируйтесь')
    button_back = Button(text = 'Назад', command = choise)
    log_title = Label(text = 'Введите Ваш логин')
    reg_login = Entry()
    title_password1 = Label(text = 'Введите Ваш пароль')
    reg_password1 = Entry()
    title_password2 = Label(text = 'Еще раз пароль:')
    reg_password2 = Entry(show = '*')
    button_regist = Button(text = 'Зарегистрироваться', command = lambda: reg(reg_login.get(), reg_password1.get(), reg_password2.get()))
    main_title.pack()
    button_back.pack()
    log_title.pack()
    reg_login.pack()
    title_password1.pack()
    reg_password1.pack()
    title_password2.pack()
    reg_password2.pack()
    button_regist.pack()

def reg(user_login, password1, password2):
    if password1 != password2:
        messagebox.showinfo('Ошибка', 'Не удалось зарегестрироваться так как пароли не совпадают')
        registration()
    else:
        request = requests.post('http://127.0.0.1:5000/registration', json = {'login': user_login,
                                                                        'password': password1})
        if request.content == b'Success':
            login()
        elif request.content == b'Denied':
            messagebox.showinfo('Ошибка', 'Не удалось зарегестрироваться так как такой логин уже есть')
            choise()
        elif request.content == b'Denied long login':
            messagebox.showinfo('Ошибка', 'Не удалось зарегестрироваться так как логин слишком длинный')
            choise()
    
def login():
    clear()
    main_title = Label(text = 'Теперь вы можете войти в систему.')
    button_back = Button(text = 'Назад', command = choise)
    login_title = Label(text = 'Введите ваш логин: ')
    reg_login = Entry()
    password_title = Label(text = 'Введите ваш пароль: ')
    reg_password = Entry(show = '*')
    button_enter = Button(text = 'Войти', command = lambda: log(reg_login.get(), reg_password.get()))
    main_title.pack()
    button_back.pack()
    login_title.pack()
    reg_login.pack()
    password_title.pack()
    reg_password.pack()
    button_enter.pack()

def log(user_login, user_password):
    request = requests.post('http://127.0.0.1:5000/login', json = {'login': user_login,
                                                         'password': user_password})
    if request.content == b'Success':
        if len(login_password_id__array) >= 2:
            for i in range(len(login_password_id__array)):
                login_password_id__array.pop(0)
        login_password_id__array.append(user_login)
        login_password_id__array.append(user_password)
        main_menu()
    elif request.content == b'Denied':
        messagebox.showinfo('Ошибка', 'войти так как не удалось найти совпадения')
        login()

choise()
root.mainloop()