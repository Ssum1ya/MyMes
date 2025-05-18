def split_message_by_words(msg, length=63):
    words = msg.split()
    lines = []
    current_line = ""
    for word in words:
        if len(current_line) + len(word) + 1 <= length:
            current_line += (word + " ")
        else:
            lines.append(current_line.rstrip())
            current_line = word + " "
    if current_line:
        lines.append(current_line.rstrip())
    return lines