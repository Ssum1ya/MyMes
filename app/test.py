from tkinter import Tk, Label, Button, Entry, Listbox, Frame, Scrollbar, Text, PhotoImage, Canvas
from tkinter import RIGHT, LEFT, BOTH, Y, END, CENTER, VERTICAL, W, E, N, S
from tkinter import messagebox

root = Tk()
root.title('My chats')
root.geometry('400x600')
root.configure(bg = "#fff")
root.resizable(False, False)

v = Scrollbar(orient=VERTICAL)
canvas = Canvas(scrollregion=(0, 0, 2000, 2000), bg="white", yscrollcommand=v.set, height = 400)
v["command"] = canvas.yview

canvas.grid(column=0, row=0, sticky=(N,W,E,S))
v.grid(column=1, row=0, sticky=(N,S))
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)

canvas.place(x = 0, y = 0)

string = '' 
lines = [string[i:i+36] for i in range(0, len(string), 36)]
print(len(string))
print(lines)
x_canvas = 375
y1 = 20 # 20
y2 = 50
if len(lines) > 1:
    y2 += 12 * len(lines) - 1
if len(lines) == 1 and len(lines[0]) < 36:
    x_canvas -= 10 * (36 - len(lines[0]))
# y2 += 50
canvas.create_rectangle(5, y1, x_canvas, y2, fill="#80CBC4", outline="#004D40") #375
y1_string = y1 + 5
for i in lines:
    canvas.create_text(10, y1_string, anchor = "nw", text=i, fill="#004D40", font=("Courier", 12))
    y1_string += 15
# canvas.create_text(len(string) * 3, y1 + 20, text=string, fill="#004D40") # 184
# canvas.create_text(10, y1 + 5, anchor = "nw", text=string, fill="#004D40", font=("Courier", 12))
# canvas.create_text(10, y1 + 20, anchor = "nw", text=string, fill="#004D40", font=("Courier", 12))

y1 = y2 + 10
y2 = y1 + 50

canvas.create_rectangle(100, y1, 300, y2 + 50, fill="#80CBC4", outline="#004D40")

# y1 = 20
# y2 = 60
# for i in range(10):
#     canvas.create_rectangle(100, y1, 300, y2, fill="#80CBC4", outline="#004D40")
#     canvas.create_text(160, y1 + 20, text="Hello METANIT.COM", fill="#004D40")
#     y1 += 50
#     y2 += 50

root.mainloop()