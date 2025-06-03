from tkinter import *
from tkinter import ttk
from tkinter import filedialog

root = Tk()
root.title("METANIT.COM")
root.geometry("250x200")

def open_file():
    filepath = filedialog.askopenfilename()
    if filepath != "":
        with open(filepath, "rb") as file:
            text = file.read()
            print(text)


open_button = ttk.Button(text="Открыть файл", command=open_file)
open_button.grid(column=0, row=1, sticky=NSEW, padx=10)

root.mainloop()