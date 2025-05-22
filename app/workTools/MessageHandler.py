from re import sub

class MessageHandler:
    @staticmethod
    def check_spaces(message):
        count = 0
        len_message = len(message)

        for i in range(len(message)):
            if message[i] == ' ':
                count += 1

        if count == len_message:
            return 'Denied'
        else:
            return 'Success'
        
    @staticmethod
    def handle_message(message):
        string = message
        string = message.replace(',', ' ')
        string = sub(r'\s+', ' ', string)
        return string