from tkinter import Label, Button, Frame

class FilesWindow:
    last_page = 0
    def __init__(self, root, files_array, chat, page, pages = None, download_file = None, login1 = None, login2 = None):
        self.window = root
        self.files_array = files_array
        self.chat = chat
        self.page = page
        self.pages = pages
        self.download_file = download_file
        self.login1 = login1
        self.login2 = login2

    def clear(self):
        for widget in self.window.winfo_children():
            widget.destroy()
    
    def draw(self):
        self.clear()

        frame = Frame(self.window, width = 350, height = 600, bg = "white")
        frame.place(x = 0, y = 0)

        heading = Label(frame, text = 'Ваши вложения', fg = '#57a1f8', bg = 'white', font = ('Microsoft YaHei UI Light', 23, 'bold'))
        heading.place(x = 100, y = 10)
        
        y = 70
        if len(self.files_array) != 0:
            for i in range(len(self.files_array)):
                user_button = Button(frame, width = 39, pady = 7, text = self.files_array[i], bg = '#57a1f8', fg = 'white', border = 0)
                user_button['command'] = lambda name = self.files_array[i]: self.download_file(self.login1, self.login2, name)
                user_button.place(x = 65, y = y)
                y += 50
        
        if self.page == 1:
            Button(frame, width = 10, pady = 7, text = 'Назад', bg = '#57a1f8', fg = 'white', border = 0, command = lambda : self.chat(self.login2)).place(x = 25, y = y)
        if self.page != 1:
            Button(frame, width = 10, pady = 7, text = 'Назад', bg = '#57a1f8', fg = 'white', border = 0, command = self.pages[self.page - 1].draw).place(x = 25, y = y)
        if self.page != FilesWindow.last_page:
             Button(frame, width = 17, pady = 7, text = 'Следущая страница', bg = '#57a1f8', fg = 'white', border = 0, command = self.pages[self.page + 1].draw).place(x = 220, y = y)