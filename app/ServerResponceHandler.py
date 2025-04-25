class ServerResponceHandler:
    @staticmethod
    def message_handler(messages):
        messages_array = messages[1: -2].split(',')
        lenght = len(messages_array)

        message_mas = []
        login1_mas = []

        for i in range(0, lenght, 2):
            login1_mas.append(messages_array[i][10: -1])

        for i in range(1, lenght, 2):
            if i == lenght - 1:
                message_mas.append(messages_array[i][6 : -6].encode('utf-8').decode('unicode_escape'))
            else:
                message_mas.append(messages_array[i][6 : -5].encode('utf-8').decode('unicode_escape'))

        return login1_mas, message_mas
    
    @staticmethod
    def chats_handler(messages):
        messages_array = messages[1: -2].split(',')
        lenght = len(messages_array)

        chats_mas = []
        ids_mas = []

        for i in range(0, lenght, 2):
            chats_mas.append(messages_array[i][10: -1])

        for i in range(1, lenght, 2):
            if i == lenght - 1:
                ids_mas.append(messages_array[i][5: -5])
            else:
                ids_mas.append(messages_array[i][5: -4])

        return chats_mas, ids_mas