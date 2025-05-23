from tkinter import Tk, Label, Button, Entry, Frame, Scrollbar, Text, PhotoImage, Canvas
from tkinter import END, VERTICAL, N, W, E, S
from tkinter import messagebox
import requests
import json
from threading import Thread
from time import sleep

from workTools.ServerResponceHandler import ServerResponceHandler
from workTools.ChatsWindow import ChatsWindow
from workTools.ChatLoadingMessage import ChatLoadingMessage
from workTools.MessageHandler import MessageHandler

root = Tk()
log_img = PhotoImage(file = 'app/images/login.png')
reg_img = PhotoImage(file = 'app/images/reg.png')

login_password_id__array = []
thread_flag = True

y1 = 50
y2 = 80

def clear():
    for widget in root.winfo_children():
    	widget.destroy()

def main_menu():
    global y1
    global y2
    global thread_flag
    y1 = 50
    y2 = 80
    thread_flag = False
    clear()

    root.title('Main menu')
    root.geometry('400x250')
    root.configure(bg = "#fff")
    root.resizable(False, False)

    frame = Frame(root, width = 350, height = 350, bg = "white")
    frame.place(x = 0, y = 0)

    heading = Label(frame, text = 'Главное меню', fg = '#57a1f8', bg = 'white', font = ('Microsoft YaHei UI Light', 23, 'bold'))
    heading.place(x = 90, y = 10)

    Button(frame, width = 39, pady = 7, text = 'Мои чаты', bg = '#57a1f8', fg = 'white', border = 0,command = lambda: show_my_chats()).place(x = 65, y = 80)
    Button(frame, width = 39, pady = 7, text = 'Добавить пользователя в чаты', bg = '#57a1f8', fg = 'white', border = 0, command = lambda: add_person2chats()).place(x = 65, y = 130)
    Button(frame, width = 39, pady = 7, text = 'Назад', bg = '#57a1f8', fg = 'white', border = 0, command = login).place(x = 65, y = 180)

def show_my_chats():
    clear()
    root.title('My chats')
    root.geometry('400x600')

    frame = Frame(root, width = 350, height = 600, bg = "white")
    frame.place(x = 0, y = 0)

    heading = Label(frame, text = 'Ваши чаты', fg = '#57a1f8', bg = 'white', font = ('Microsoft YaHei UI Light', 23, 'bold'))
    heading.place(x = 120, y = 10)

    request = requests.get('http://127.0.0.1:5000/users', json = {'login': login_password_id__array[0]})
    server_answer = json.loads(request.content.decode())
    data = server_answer['data']

    chats_mas = []
    ids_mas = []
    for i in range(len(data)):
        chats_mas.append(data[i][0])
        ids_mas.append(data[i][1])

    chats_mas_split = [chats_mas[i:i+9] for i in range(0, len(chats_mas), 9)]
    ids_mas_split = [ids_mas[i:i+9] for i in range(0, len(ids_mas), 9)]
    
    if len(ids_mas_split) != 0:
        pages = {1: ChatsWindow(root = root, chats_ids = [chats_mas_split[0], ids_mas_split[0]], chat = chat, page = 1, main_menu = main_menu)}
        pages[1].pages = pages
        for i in range(1, len(chats_mas_split)):
            pages[list(pages.keys())[-1] + 1] = ChatsWindow(root = root, chats_ids = [chats_mas_split[i], ids_mas_split[i]], chat = chat, page = list(pages.keys())[-1] + 1, main_menu = main_menu, pages = pages)
        
        ChatsWindow.last_page = list(pages.keys())[-1]

        pages[1].draw()
    else:
        Button(frame, width = 39, pady = 7, text = 'Назад', bg = '#57a1f8', fg = 'white', border = 0, command = main_menu).place(x = 65, y = 70)

def add_person2chats():
    clear()
    root.title('Add person to my chats')
    root.geometry('400x250')

    frame = Frame(root, width = 400, height = 400, bg = "white")
    frame.place(x = 0, y = 0)

    heading = Label(frame, text = 'Добавить пользователя', fg = '#57a1f8', bg = 'white', font = ('Microsoft YaHei UI Light', 18, 'bold'))
    heading.place(x = 50, y = 10)

    heading = Label(frame, text = 'Введите логин', fg = '#57a1f8', bg = 'white', font = ('Microsoft YaHei UI Light', 15, 'bold'))
    heading.place(x = 40, y = 60)

    person_login = Entry(frame, width = 40, fg = 'black', border = 0, bg = "white", font = ('Microsoft YaHei UI Light', 11), )
    person_login.place(x = 45, y = 100)

    Frame(frame, width = 295, height = 2, bg = 'black').place(x = 45, y = 127)

    Button(frame, width = 39, pady = 7, text = 'Добавить', bg = '#57a1f8', fg = 'white', border = 0, command = lambda : check_login_in_bd(person_login.get(), )).place(x = 55, y = 157)
    Button(frame, width = 39, pady = 7, text = 'Назад', bg = '#57a1f8', fg = 'white', border = 0, command = main_menu).place(x = 55, y = 207)

# TODO: вынести в отдельный файл
def check_login_in_bd(user_login):
    request = requests.post('http://127.0.0.1:5000/add_person2chats', json = {'chat': user_login,
                                                                              'login': login_password_id__array[0]})
    server_answer = json.loads(request.content.decode())
    answer = server_answer['answer']
    if answer == 'Success':
        messagebox.showinfo('Успех', 'пользователь успешно добавлен в ваши чаты')
        main_menu()
    elif answer == 'Denied':
        messagebox.showinfo('Ошибка', 'не удалось найти пользователя с логином')
        add_person2chats()
    elif answer == 'Denied login equals chat':
        messagebox.showinfo('Ошибка', 'ваш логин равен чату который хотите добавить')
        add_person2chats()
    elif answer == 'Denied empty string':
        messagebox.showinfo('Ошибка', 'введите не пустую строку')
        add_person2chats()
    elif answer == 'Denied already in chats':
        messagebox.showinfo('Ошибка', 'этот пользователь уже у вас в чатах')
        add_person2chats()

def chat(user_chat):
    global thread_flag
    thread_flag = True
    clear()
    root.title(user_chat)
    root.geometry('400x600')

    canvas = Canvas(bg="white", height = 400) 
    canvas.grid(column=0, row=0, sticky=(N,W,E,S))
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)
    canvas.place(x = 0, y = 0)

    frame = Frame(root, width = 380, height = 400, bg = "white")
    frame.place(x = 0, y = 400)   

    entry_field = Text(height=5, wrap="char")

    Frame(frame, width = 400, height = 2, bg = 'black').place(x = 0, y = 90)
    Button(frame, width = 39, pady = 7, text = 'Отправить', bg = '#57a1f8', fg = 'white', border = 0, command = lambda: send_message(entry_field.get("1.0", END), canvas, user_chat, entry_field)).place(x = 55, y = 100)
    Button(frame, width = 39, pady = 7, text = 'Назад', bg = '#57a1f8', fg = 'white', border = 0, command = main_menu).place(x = 55, y = 150)

    root.protocol("WM_DELETE_WINDOW")
    login1_mas, message_mas = show_history_messages(user_chat)

    canvas.create_text(0, 0, anchor = "nw", text='Цвет ваших сообщений', fill="#57a1f8", font=("Courier", 12)) 
    canvas.create_text(0, 15, anchor = "nw", text='Цвет - ' + user_chat, fill="#00FF00", font=("Courier", 12))
    canvas.create_text(100, 30, anchor = "nw", text='Начало переписки', fill="#000000", font=("Courier", 12))

    global y1 
    global y2
    for i in range(len(message_mas)):
        login1 = login1_mas[i]
        message = message_mas[i]
        y1, y2 = ChatLoadingMessage.load_message(canvas, login1, message, y1, y2, login_password_id__array[0])

        y1 = y2 + 10
        y2 = y1 + 30

    v = Scrollbar(orient=VERTICAL)
    canvas['scrollregion'] = (0, 0, y2, y2)
    canvas['yscrollcommand'] = v.set
    v["command"] = canvas.yview
    v.grid(column=1, row=0, sticky=(N,S))
    entry_field.grid(padx = 0, pady = 120)

    canvas.yview_moveto(1)
    
    loading_history_thread = Thread(target = lambda: load_new_message(canvas, user_chat))
    loading_history_thread.start()

def load_new_message(canvas, user_chat):
    global y1 
    global y2
    flag = True              
    while flag and thread_flag:
        sleep(2)
        request = requests.post('http://127.0.0.1:5000/get_new_messages', json = {'login1' : user_chat, 
                                                                          'login2': login_password_id__array[0]})
        messages = request.content.decode()
        login1_mas, message_mas = ServerResponceHandler.message_handler(messages)

        for i in range(len(message_mas)):
            login1 = login1_mas[i]
            message = message_mas[i]
            try:
                y1, y2 = ChatLoadingMessage.load_message(canvas, login1, message, y1, y2, login_password_id__array[0])

                y1 = y2 + 10
                y2 = y1 + 30

                canvas['scrollregion'] = (0, 0, y2, y2)
                canvas.yview_moveto(1)
            except:
                flag = False

def send_message(message, canvas, user_chat, entry_field):
    global y1
    global y2

    message = MessageHandler.handle_message(message.strip())
    answer = MessageHandler.check_spaces(message)

    if answer == 'Denied':
        messagebox.showinfo('Отклонено', 'Ваще сообщение состоит из пробелов')
    else:
        message = message.strip()
        request = requests.post('http://127.0.0.1:5000/send_message', json = {'login1': login_password_id__array[0],
                                                                                        'login2': user_chat,
                                                                                        'text': message})
        check = check_message(request.content)
        if check == 'Success':
            lines = [message[i:i+36] for i in range(0, len(message), 36)]
            x_canvas = 375

            if len(lines) > 1:
                y2 += 12 * len(lines) - 1
            if len(lines) == 1 and len(lines[0]) < 36:
                x_canvas -= 10 * (36 - len(lines[0]))

            canvas.create_rectangle(5, y1, x_canvas, y2, fill="#57a1f8", outline="#000000")

            y1_string = y1 + 5
            for i in lines:
                canvas.create_text(10, y1_string, anchor = "nw", text=i, fill="#004D40", font=("Courier", 12))
                y1_string += 15

            y1 = y2 + 10
            y2 = y1 + 30

            canvas['scrollregion'] = (0, 0, y2, y2)
            canvas.yview_moveto(1)

            entry_field.delete("1.0", END)

# TODO: вынести в отдельный файл
def check_message(server_answer):
    if server_answer == b'Denied empty message':
        messagebox.showinfo('Отклонено', 'Ваще сообщение путстое')
    elif server_answer == b'Denied long message':
        messagebox.showinfo('Отклонено', 'Слишком большое сообщение')
    else:
        return 'Success'
    
# TODO: вынести в отдельный файл
def show_history_messages(user_chat):
    request = requests.post('http://127.0.0.1:5000/get_history', json = {'login1': login_password_id__array[0],
                                                                                     'login2': user_chat})
    messages = request.content.decode()
    login1_mas, message_mas = ServerResponceHandler.message_handler(messages)
    
    return login1_mas, message_mas

def login():
    clear()
    root.title('Login')
    root.geometry('925x500+300+200')
    root.configure(bg = "#fff")
    root.resizable(False, False)

    Label(root, image = log_img, bg = 'white').place(x = 50, y = 50)

    frame = Frame(root, width = 350, height = 350, bg = "white")
    frame.place(x = 480, y = 70)

    heading = Label(frame, text = 'Вход', fg = '#57a1f8', bg = 'white', font = ('Microsoft YaHei UI Light', 23, 'bold'))
    heading.place(x = 110, y = 5)

    heading = Label(frame, text = 'Имя пользователя', fg = '#57a1f8', bg = 'white', font = ('Microsoft YaHei UI Light', 11, 'bold'))
    heading.place(x = 20, y = 50)

    user = Entry(frame, width = 25, fg = 'black', border = 0, bg = "white", font = ('Microsoft YaHei UI Light', 11), )
    user.place(x = 30, y = 80)

    Frame(frame, width = 295, height = 2, bg = 'black').place(x = 25, y = 107)

    heading = Label(frame, text = 'Пароль', fg = '#57a1f8', bg = 'white', font = ('Microsoft YaHei UI Light', 11, 'bold'))
    heading.place(x = 20, y = 120)

    code = Entry(frame, width = 25, fg = 'black', border = 0, bg = 'white', font = ('Microsoft YaHei UI Light', 11), show = '*')
    code.place(x = 30, y = 150) 

    Frame(frame, width = 295, height = 2, bg = 'black').place(x = 25, y = 177)

    Button(frame, width = 39, pady = 7, text = 'Войти', bg = '#57a1f8', fg = 'white', border = 0, command = lambda: log(user.get(), code.get())).place(x = 35, y = 204)
    label = Label(frame, text = "Нет учетной записи?", fg = 'black', bg = 'white', font = ('Microsoft YaHei UI Light', 9))
    label.place(x = 35, y = 270)

    sign_up = Button(frame, width = 19, text = 'Зарегистрироваться', border = 0, bg = 'white', cursor = 'hand2', fg = '#57a1f8', command = registration)
    sign_up.place(x = 165, y = 270)

# TODO: вынести в отдельный файл
def reg(user_login, password1, password2):
    if password1 != password2:
        messagebox.showinfo('Ошибка', 'Не удалось зарегистрироваться так как пароли не совпадают')
        registration()
    else:
        request = requests.post('http://127.0.0.1:5000/registration', json = {'login': user_login,
                                                                        'password': password1})
        server_answer = json.loads(request.content.decode())
        answer = server_answer['answer']
        if answer == 'Success':
            messagebox.showinfo('Успешно', 'Теперь войдите под своей учетной записью')
            login()
        elif answer == 'Denied':
            messagebox.showinfo('Ошибка', 'Не удалось зарегистрироваться так как такой логин уже есть')
            registration()
        elif answer == 'Denied long login':
            messagebox.showinfo('Ошибка', 'Не удалось зарегистрироваться так как логин слишком длинный')
            registration()
    
def registration():
    clear()
    root.title('Registration')
    root.geometry('925x500+300+200')

    Label(root, image = reg_img, bg = 'white').place(x = 50, y = 50)

    frame = Frame(root, width = 350, height = 350, bg = "white")
    frame.place(x = 480, y = 70)

    heading = Label(frame, text = 'Регистрация', fg = '#57a1f8', bg = 'white', font = ('Microsoft YaHei UI Light', 23, 'bold'))
    heading.place(x = 80, y = 5)

    heading = Label(frame, text = 'Имя пользователя', fg = '#57a1f8', bg = 'white', font = ('Microsoft YaHei UI Light', 11, 'bold'))
    heading.place(x = 20, y = 50)

    user = Entry(frame, width = 25, fg = 'black', border = 0, bg = "white", font = ('Microsoft YaHei UI Light', 11))
    user.place(x = 30, y = 80)

    Frame(frame, width = 295, height = 2, bg = 'black').place(x = 25, y = 107)

    code = Entry(frame, width = 25, fg = 'black', border = 0, bg = 'white', font = ('Microsoft YaHei UI Light', 11), show = '*')
    code.place(x = 30, y = 150)

    heading = Label(frame, text = 'Пароль', fg = '#57a1f8', bg = 'white', font = ('Microsoft YaHei UI Light', 11, 'bold'))
    heading.place(x = 20, y = 120) 

    Frame(frame, width = 295, height = 2, bg = 'black').place(x = 25, y = 177)

    heading = Label(frame, text = 'Подтвердить пароль', fg = '#57a1f8', bg = 'white', font = ('Microsoft YaHei UI Light', 11, 'bold'))
    heading.place(x = 20, y = 190) 

    conform_code = Entry(frame, width = 25, fg = 'black', border = 0, bg = 'white', font = ('Microsoft YaHei UI Light', 11), show = '*')
    conform_code.place(x = 30, y = 220) 

    Frame(frame, width = 295, height = 2, bg = 'black').place(x = 25, y = 247)
    
    Button(frame, width = 39, pady = 7, text = 'Зарегестрироваться', bg = '#57a1f8', fg = 'white', border = 0, command = lambda: reg(user.get(), code.get(), conform_code.get())).place(x = 35, y = 280)
    label = Label(frame, text = "Уже есть учетная запись?", fg = 'black', bg = 'white', font = ('Microsoft YaHei UI Light', 9))
    label.place(x = 40, y = 320)

    sign_up = Button(frame, width = 5, text = 'Войти', border = 0, bg = 'white', cursor = 'hand2', fg = '#57a1f8', command = login)
    sign_up.place(x = 200, y = 320)

# TODO: вынести в отдельный файл
def log(user_login, user_password):
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
        main_menu()
    elif answer == 'Denied':
        messagebox.showinfo('Ошибка', 'Не удалось найти совпадения')
        login()

login()

root.mainloop()