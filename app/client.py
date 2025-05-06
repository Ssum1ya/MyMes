from tkinter import Tk, Label, Button, Entry, Listbox, Frame, Scrollbar, Text, PhotoImage
from tkinter import RIGHT, LEFT, BOTH, Y, END
from tkinter import messagebox
import requests
from threading import Thread
from time import sleep

from ServerResponceHandler import ServerResponceHandler

root = Tk()
log_img = PhotoImage(file = 'app/images/login.png')
reg_img = PhotoImage(file = 'app/images/reg.png')

# root.geometry('400x600')
# root.title('Войти в систему')

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
    scrollbar = Scrollbar(messages_frame)

    msg_list = Listbox(messages_frame, height = 15, width = 50, yscrollcommand = scrollbar.set)
    scrollbar.pack(side = RIGHT, fill = Y)
    msg_list.pack(side = LEFT, fill = BOTH)
    msg_list.pack()
    messages_frame.pack()

    button_back = Button(text = 'Назад', command = main_menu)

    entry_field = Text(height=5, wrap="char")
    entry_field.pack()

    send_button = Button(root, text = 'отправить', command = lambda: send_message(entry_field.get("1.0", END), msg_list, user_chat, entry_field))
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

def send_message(message, msg_list, user_chat, entry_field):
    request = requests.post('http://127.0.0.1:5000/send_message', json = {'login1': login_password_id__array[0],
                                                                                     'login2': user_chat,
                                                                                     'text': message})
    msg_list.insert(END, f'{login_password_id__array[0]} : {message}')
    msg_list.yview_scroll(number = 1, what = 'units')
    entry_field.delete("1.0", END)

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

def login():
    clear()
    root.title('Login')
    root.geometry('925x500+300+200')
    root.configure(bg = "#fff")
    root.resizable(False, False)

    Label(root, image = log_img, bg = 'white').place(x = 50, y = 50)

    frame = Frame(root, width = 350, height = 350, bg = "white")
    frame.place(x = 480, y = 70)

    heading = Label(frame, text = 'Sign in', fg = '#57a1f8', bg = 'white', font = ('Microsoft YaHei UI Light', 23, 'bold'))
    heading.place(x = 100, y = 5)

    def on_enter(e):
        user.delete(0, 'end')

    def on_leave(e):
        name = user.get()
        if name == '':
            user.insert(0, 'Username')

    user = Entry(frame, width = 25, fg = 'black', border = 0, bg = "white", font = ('Microsoft YaHei UI Light', 11))
    user.place(x = 30, y = 80)
    user.insert(0, 'Username')
    user.bind('<FocusIn>', on_enter)
    user.bind('<FocusOut>', on_leave)

    Frame(frame, width = 295, height = 2, bg = 'black').place(x = 25, y = 107)


    def on_enter(e):
        code.delete(0, 'end')

    def on_leave(e):
        name = code.get()
        if name == '':
            code.insert(0, 'Password')

    code = Entry(frame, width = 25, fg = 'black', border = 0, bg = 'white', font = ('Microsoft YaHei UI Light', 11))
    code.place(x = 30, y = 150) 
    code.insert(0, 'Password')
    code.bind('<FocusIn>', on_enter)
    code.bind('<FocusOut>', on_leave)

    Frame(frame, width = 295, height = 2, bg = 'black').place(x = 25, y = 177)

    Button(frame, width = 39, pady = 7, text = 'Sign in', bg = '#57a1f8', fg = 'white', border = 0, command = lambda: log(user.get(), code.get())).place(x = 35, y = 204)
    label = Label(frame, text = "Don't have an account?", fg = 'black', bg = 'white', font = ('Microsoft YaHei UI Light', 9))
    label.place(x = 75, y = 270)

    sign_up = Button(frame, width = 6, text = 'Sign up', border = 0, bg = 'white', cursor = 'hand2', fg = '#57a1f8', command = registration)
    sign_up.place(x = 215, y = 270)

def reg(user_login, password1, password2):
    if password1 != password2:
        messagebox.showinfo('Ошибка', 'Не удалось зарегестрироваться так как пароли не совпадают')
        registration()
    else:
        request = requests.post('http://127.0.0.1:5000/registration', json = {'login': user_login,
                                                                        'password': password1})
        if request.content == b'Success':
            messagebox.showinfo('Успешно', 'Теперь войдите под своей учетной записью')
            login()
        elif request.content == b'Denied':
            messagebox.showinfo('Ошибка', 'Не удалось зарегестрироваться так как такой логин уже есть')
            registration()
        elif request.content == b'Denied long login':
            messagebox.showinfo('Ошибка', 'Не удалось зарегестрироваться так как логин слишком длинный')
            registration()
    
def registration():
    clear()
    root.title('Registration')
    root.geometry('925x500+300+200')
    root.configure(bg = "#fff")
    root.resizable(False, False)

    Label(root, image = reg_img, bg = 'white').place(x = 50, y = 50)

    frame = Frame(root, width = 350, height = 350, bg = "white")
    frame.place(x = 480, y = 70)

    heading = Label(frame, text = 'Sign up', fg = '#57a1f8', bg = 'white', font = ('Microsoft YaHei UI Light', 23, 'bold'))
    heading.place(x = 100, y = 5)

    def on_enter(e):
        user.delete(0, 'end')

    def on_leave(e):
        name = user.get()
        if name == '':
            user.insert(0, 'Username')

    user = Entry(frame, width = 25, fg = 'black', border = 0, bg = "white", font = ('Microsoft YaHei UI Light', 11))
    user.place(x = 30, y = 80)
    user.insert(0, 'Username')
    user.bind('<FocusIn>', on_enter)
    user.bind('<FocusOut>', on_leave)

    Frame(frame, width = 295, height = 2, bg = 'black').place(x = 25, y = 107)


    def on_enter(e):
        code.delete(0, 'end')

    def on_leave(e):
        name = code.get()
        if name == '':
            code.insert(0, 'Password')

    code = Entry(frame, width = 25, fg = 'black', border = 0, bg = 'white', font = ('Microsoft YaHei UI Light', 11))
    code.place(x = 30, y = 150) 
    code.insert(0, 'Password')
    code.bind('<FocusIn>', on_enter)
    code.bind('<FocusOut>', on_leave)

    Frame(frame, width = 295, height = 2, bg = 'black').place(x = 25, y = 177)

    def on_enter(e):
        conform_code.delete(0, 'end')

    def on_leave(e):
        name = conform_code.get()
        if name == '':
            conform_code.insert(0, 'Password')

    conform_code = Entry(frame, width = 25, fg = 'black', border = 0, bg = 'white', font = ('Microsoft YaHei UI Light', 11))
    conform_code.place(x = 30, y = 220) 
    conform_code.insert(0, 'Confrom Password')
    conform_code.bind('<FocusIn>', on_enter)
    conform_code.bind('<FocusOut>', on_leave)

    Frame(frame, width = 295, height = 2, bg = 'black').place(x = 25, y = 247)

    Button(frame, width = 39, pady = 7, text = 'Sign in', bg = '#57a1f8', fg = 'white', border = 0, command = lambda: reg(user.get(), code.get(), conform_code.get())).place(x = 35, y = 280)
    label = Label(frame, text = "I have an account", fg = 'black', bg = 'white', font = ('Microsoft YaHei UI Light', 9))
    label.place(x = 90, y = 320)

    sign_up = Button(frame, width = 6, text = 'Sign in', border = 0, bg = 'white', cursor = 'hand2', fg = '#57a1f8', command = login)
    sign_up.place(x = 200, y = 320)

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

login()

root.mainloop()