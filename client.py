from tkinter import *
from tkinter import messagebox
import requests

root = Tk()
root.geometry('400x600')
root.title('Войти в систему')

def clear():
    for widget in root.winfo_children():
    	widget.destroy()

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
    button_registr = Button(text = 'Зарегистрироваться')
    main_title.pack()
    button_back.pack()
    log_title.pack()
    reg_login.pack()
    title_password1.pack()
    reg_password1.pack()
    title_password2.pack()
    reg_password2.pack()
    button_registr.pack()
    
    if reg_login and reg_password1:
        r = requests.post('http://127.0.0.1:5000/registration', json = {'login': reg_login,
                                                                    'password': reg_password1})
    

def login():
    clear()
    main_title = Label(text = 'Теперь вы можете войти в систему.')
    button_back = Button(text = 'Назад', command = choise)
    login_title = Label(text = 'Введите ваш логин: ')
    reg_login = Entry()
    password_title = Label(text = 'Введите ваш пароль: ')
    reg_password = Entry(show = '*')
    button_enter = Button(text = 'Войти')
    main_title.pack()
    button_back.pack()
    login_title.pack()
    reg_login.pack()
    password_title.pack()
    reg_password.pack()
    button_enter.pack()

choise()
root.mainloop()