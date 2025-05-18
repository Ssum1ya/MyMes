string = 'asdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasd asdasd asd asdas asdasadsdasd asdasdas saasdasdasd asdasdasdasasd asd asd asd '
login1 = 'Aokihary'
def parse_string(string, login1):
    rows = []
    rows.append(string[0: 63 - len(login1) - 1]) # rows.append(string[0: 63 - len(login1) - 3])
    for i in range(63 - len(login1) - 3, len(string), 63):
        rows.append(string[i: i + 63])
    return rows

array = parse_string(string = string,  login1 = login1)
print(len(array[0]), len(array[1]))
print(len('Aokihary : asdkfsadhkfasjkfhksadjfaslkfhaskfhkadshfksadlhfkasdhfk'))