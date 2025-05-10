from tkinter import Tk, Label, Button, Entry, Listbox, Frame, Scrollbar, Text, PhotoImage
from tkinter import RIGHT, LEFT, BOTH, Y, END
from tkinter import messagebox

class ChatsWindow:
    last_page = 0
    def __init__(self, root, chats_ids, chat, page, main_menu, pages = None):
        self.window = root
        self.log_img = PhotoImage(file = 'app/images/login.png')
        self.window.title('My chats')
        self.window.geometry('400x600')
        self.window.configure(bg = "#fff")
        self.window.resizable(False, False)
        self.chats_ids = chats_ids
        self.chat = chat
        self.page = page
        self.main_menu = main_menu
        self.pages = pages

    def clear(self):
        for widget in self.window.winfo_children():
            widget.destroy()
    
    def draw(self):
        self.clear()

        frame = Frame(self.window, width = 350, height = 600, bg = "white")
        frame.place(x = 0, y = 0)

        heading = Label(frame, text = 'Ваши чаты', fg = '#57a1f8', bg = 'white', font = ('Microsoft YaHei UI Light', 23, 'bold'))
        heading.place(x = 120, y = 10)
        
        self.chats_mas = self.chats_ids[0]
        self.ids_mas = self.chats_ids[1]
        y = 70
        if len(self.ids_mas) != 0:
            for i in range(len(self.chats_mas)):
                if self.ids_mas[i] == '1':
                    user_button = Button(frame, width = 39, pady = 7, text = self.chats_mas[i], bg = '#00FF00', fg = 'black', border = 0)
                    user_button['command'] = lambda user_chat = self.chats_mas[i]: self.chat(user_chat)
                    user_button.place(x = 65, y = y)
                else:
                    user_button = Button(frame, width = 39, pady = 7, text = self.chats_mas[i], bg = '#57a1f8', fg = 'white', border = 0)
                    user_button['command'] = lambda user_chat = self.chats_mas[i]: self.chat(user_chat)
                    user_button.place(x = 65, y = y)
                y += 50
        
        if self.page == 1:
            Button(frame, width = 10, pady = 7, text = 'Назад', bg = '#57a1f8', fg = 'white', border = 0, command = self.main_menu).place(x = 25, y = y)
        if self.page != 1:
            Button(frame, width = 10, pady = 7, text = 'Назад', bg = '#57a1f8', fg = 'white', border = 0, command = self.pages[self.page - 1].draw).place(x = 25, y = y)
        if self.page != ChatsWindow.last_page:
             Button(frame, width = 17, pady = 7, text = 'Следущая страница', bg = '#57a1f8', fg = 'white', border = 0, command = self.pages[self.page + 1].draw).place(x = 220, y = y)
        