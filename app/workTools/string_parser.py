# string = 'asddddddddddddddddddddddddddd dddddddddddddddddddqqqqqqqqqqqqqqqqqqqqqqqqqq qqqqqqqqqqqqqqqqqqqqww wwwwwwwwwwwwwwwwwwwwwwwwwwwwasdddddddddddddddddddddddddddddddddddddddddddddddddddddddddd'
# login1 = 'login1'
def parse_string(string, login1):
    rows = []
    rows.append(string[0: 57 - len(login1) - 3]) # rows.append(string[0: 63 - len(login1) - 3])
    for i in range(57 - len(login1) - 3, len(string), 57):
        rows.append(string[i: i + 57])
    return rows

# array = parse_string(string = string, login1 = login1)
# print(array)
# print(len(array[0]), len(array[3]))