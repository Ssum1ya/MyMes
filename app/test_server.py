from flask import Flask, request, send_file

app = Flask("server")
file_name = 'kiyotaka.jpg'

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return send_file(file_name, as_attachment = True, download_name = 'zxc.jpg')
    elif request.method == 'POST':
        pass

if __name__ == '__main__':
    app.run(debug = True)