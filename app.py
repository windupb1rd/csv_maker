from flask import Flask, request, render_template, url_for, send_from_directory

import database
import make_scvs

app = Flask(__name__)  # инициализация инстанса приложения


@app.route('/')  # The association between a URL and the function that handles it is called a route.
def index():     # it is called a view function
    user_agent = request.headers.get('User-Agent')  # The request object, which encapsulates
                                                    # the contents of an HTTP request sent by the client.
    print(url_for('index', _external=True))         # создает путь
    return render_template("index.html")  # шаблоны должны находится в папке templates на этом же уровне

def auth(func):
    def wrapper(*args, **kwargs):
        if not request.authorization:
            return ('Unauthorized', 401, {'WWW-Authenticate': 'Basic realm="admin"'})
        elif request.authorization and (request.authorization.username != 'user1' or request.authorization.password != '1234'):
            return ('Invalid user', 401, {'WWW-Authenticate': 'Basic realm="admin"'})
        else:
            print('auth dec worked')
            return func(*args, **kwargs)
    wrapper.__name__ = func.__name__  # не понял почему нужно менять имя
    return wrapper


@app.route('/form_csv')
def form_csv():
    return render_template('form_csv.html')


@app.route('/paste', methods=['POST', 'GET'])  # метод POST обязательно явно указывать
def paste():
    data = request.form['userdata']
    result = make_scvs.start_making_csv_from_web(data)
    return render_template('paste.html', result=result[2], filename=f'{result[0]}.zip')


@app.route('/download/<filename>')
def download(filename):
    return send_from_directory('files/', f'{filename}')


@app.route('/log')
@auth
def get_log():
    result = database.select_from_db()
    return render_template('log.html', result=result)


# app.add_url_rule('/', 'index', index)  # способ вызова функций без декоратора

# start, option used for tests, not deploying
# if __name__ == '__main__':
#     app.run(debug=True)

# start app from console, more preferable option
# (venv) $ export FLASK_APP=hello.py  # necessary
# (venv) $ export FLASK_DEBUG=1  # optional, enables debugging mode after an exception
# (venv) $ flask run  # necessary
# (venv) $ flask run --host 0.0.0.0  # run on a custom host
# * Serving Flask app "hello"
# * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
