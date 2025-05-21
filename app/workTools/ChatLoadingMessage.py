class ChatLoadingMessage:
    @staticmethod
    def load_message(canvas, login1, message, y1, y2, self_login):
        lines = [message[i:i+36] for i in range(0, len(message), 36)]
        x_canvas = 375

        if len(lines) > 1:
            y2 += 12 * len(lines) - 1
        if len(lines) == 1 and len(lines[0]) < 36:
            x_canvas -= 10 * (36 - len(lines[0]))

        if login1 == self_login:
            canvas.create_rectangle(5, y1, x_canvas, y2, fill="#57a1f8", outline="#000000") #375 #57a1f8 #00FF00 #000F4D
        else:
            canvas.create_rectangle(5, y1, x_canvas, y2, fill="#00FF00", outline="#000000")

        y1_string = y1 + 5
        for i in lines:
            canvas.create_text(10, y1_string, anchor = "nw", text=i, fill="#004D40", font=("Courier", 12))
            y1_string += 15
            
        return y1, y2