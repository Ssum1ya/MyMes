from tkinter import *
from tkinter import ttk, messagebox
from tkinter import filedialog
import requests
import base64
import json

root = Tk()
root.title("METANIT.COM")
root.geometry("250x200")

login1 = 'zxc'
login2 = 'Aokihary'

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

open_button = ttk.Button(text="Открыть файл", command=send_file)
open_button.grid(column=0, row=1, sticky=NSEW, padx=10)

root.mainloop()