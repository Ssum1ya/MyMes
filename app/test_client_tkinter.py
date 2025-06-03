from tkinter import *
from tkinter import ttk, messagebox
from tkinter import filedialog
import requests
import base64
import json
from workTools.FilesWindow import FilesWindow

root = Tk()
root.title("METANIT.COM")
root.geometry("250x200")

login1 = 'zxc'
login2 = 'Aokihary'

def clear():
    for widget in root.winfo_children():
    	widget.destroy()

def send_file():
    filepath = filedialog.askopenfilename()
    if filepath != "":
        file_name = filepath.split('/')[-1]
        with open(filepath, "rb") as file:
            data = file.read()
            data_b64 = base64.b64encode(data).decode('utf-8')
            request = requests.post('http://127.0.0.1:5000/send_files', json = {'login1' : login1,
                                                                     'login2' : login2,
                                                                     'file_name' : file_name,
                                                                     'file_data' : data_b64})
            server_answer = json.loads(request.content.decode())
            answer = server_answer['answer']
            if answer == 'Denied':
                messagebox.showinfo('Ошибка', 'Файл с таким названием уже есть')
            else:
                messagebox.showinfo('Успешно', 'Файл отправлен')

def get_files():
    clear()
    root.title('My chats')
    root.geometry('400x600')

    frame = Frame(root, width = 350, height = 600, bg = "white")
    frame.place(x = 0, y = 0)

    heading = Label(frame, text = 'Ваши вложения', fg = '#57a1f8', bg = 'white', font = ('Microsoft YaHei UI Light', 23, 'bold'))
    heading.place(x = 120, y = 10)

    request = requests.get('http://127.0.0.1:5000/send_files', json = {'login1' : login1,
                                                                       'login2' : login2})
    server_answer = json.loads(request.content.decode())
    data = server_answer['data']

    data_split = [data[i:i+9] for i in range(0, len(data), 9)]

    if len(data_split) != 0:
        pages = {1: FilesWindow(root = root, files_array = data_split[0], chat = chat, page = 1)}
        pages[1].pages = pages
        for i in range(1, len(data_split)):
            pages[list(pages.keys())[-1] + 1] = FilesWindow(root = root, files_array = data_split[i], chat = chat, page = list(pages.keys())[-1] + 1, pages = pages)
        
        FilesWindow.last_page = list(pages.keys())[-1]

        pages[1].draw()
    else:
        Button(frame, width = 39, pady = 7, text = 'Назад', bg = '#57a1f8', fg = 'white', border = 0, command = chat).place(x = 65, y = 70)


def chat():
    clear()
    root.title('chat')
    root.geometry('400x700')
    root.configure(bg = "#fff")
    root.resizable(False, False)

    canvas = Canvas(bg="white", height = 400) 
    canvas.grid(column=0, row=0, sticky=(N,W,E,S))
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)
    canvas.place(x = 0, y = 0)

    frame = Frame(root, width = 380, height = 400, bg = "white")
    frame.place(x = 0, y = 400)   

    entry_field = Text(height=5, wrap="char")

    Frame(frame, width = 400, height = 2, bg = 'black').place(x = 0, y = 90)
    Button(frame, width = 39, pady = 7, text = 'Отправить', bg = '#57a1f8', fg = 'white', border = 0).place(x = 55, y = 100)
    Button(frame, width = 39, pady = 7, text = 'Назад', bg = '#57a1f8', fg = 'white', border = 0).place(x = 55, y = 150)
    Button(frame, width = 39, pady = 7, text = 'Отправить файл', bg = '#57a1f8', fg = 'white', border = 0, command = send_file).place(x = 55, y = 200)
    Button(frame, width = 39, pady = 7, text = 'Вложения', bg = '#57a1f8', fg = 'white', border = 0, command = get_files).place(x = 55, y = 250)

chat()

root.mainloop()