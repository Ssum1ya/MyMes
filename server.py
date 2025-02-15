from flask import Flask, url_for, request

app = Flask("server")
history = []
test_reg = []

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        history.append(request.get_data())
        return request.get_data()
    else:
        try:
            return history[-1]
        except:
            return "no request"

@app.route('/registration', methods = ['GET', 'POST'])
def registration():
    if request.method == 'POST':
        test_reg.append(request.get_data())
        return request.get_data()['login']
    else:
        try:
            return test_reg[-1]
        except:
            return "no request"

if __name__ == '__main__':
    app.run(debug = True)