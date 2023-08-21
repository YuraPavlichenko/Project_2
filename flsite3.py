from flask import Flask, render_template, make_response, redirect, url_for, request, session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ngjfsbgjuh87y78yds8gbdu'  # Секретний ключ для роботи з сесіями


menu = [{'title': 'Main', "url": "/"},
        {'title': 'Add page', "url": "/add_page"}]


@app.route("/")
def index():
    # content = render_template('index.html', menu=menu, posts=[])
    # res = make_response(content)  # Отримуємо наший об'єкт запиту
    # res.headers['Content-Type'] = 'text/plain'  # Показуємо, що наша відповідь буде чисто текстом
    # res.headers['Server'] = 'flasksite'  # Дані будуть сформовані на нашому сервері, тобто на нашому додатку
    # return res  # Тобто, в такому випадку, браузер видасть нам чисто необроблений хтмл код


    # res = make_response("<h1>Помилка серсеру</h1>", 500)  # Видаємо чисто текст і номер респонса в консолі
    # return res


    # За допомогою кортежа передаємо текст, номер респонса і в хедерс тип контенту
    return ("<h1>Main Pagedsadsas</h1>", 200, {'Content-Type': 'text/plain'})


@app.route('/transfer')
def transfer():
    return redirect(url_for('index'), 301)  # Перенапраявлємо /transfer на нашу головну сторінку, тобто на index


@app.errorhandler(404)
def pageNot(error):
    return ("Сторінку не знайдено", 404)  # Повертаємо тіло відповіді та код


# @app.before_request  # Виконується перед запитом
# def before_request():
#     print("before_request() called")
#
#
# @app.after_request  # Виконується після запиту, але якщо виникне помилка, то не виконається
# def after_request(response):  # Обов'язково приймає response
#     print("after_request() called")
#     return response
#
#
# @app.teardown_request  # Виконується після запиту в будь-якому випадку, навіть якщо була помилка
# def teardown_request(response):
#     print("teardown_request() called")
#     return response


@app.route('/login')
def login():
    log = ""
    if request.cookies.get('logged'):
        log = request.cookies.get('logged')

    res = make_response(f"<h1>Форма авторизація</h1> <p>Logged: {log}")
    res.set_cookie("logged", "yes")
    return res


@app.route('/logout')
def logout():
    res = make_response(f"Ви більше не авторизовані")
    res.set_cookie("logged", "", 0)
    return res


# Дані в сесії передаються тільки тоді, коли дані якось змінюються
@app.route('/counter')
def counter():
    if 'count' in session:
        session['count'] = session.get('count') + 1
    else:
        session['count'] = 1

    return f"Ця сторінка має {session['count']} відвідувань"


data = [1, 2, 3, 4]
@app.route('/session-data')
def session_data():
    if 'data' not in session:
        session['data'] = data
    else:
        session['data'][1] += 1
        session.modified = True  # Якщо фласк думає об'єкт ніяк не змінився з попереднього запису, то треба в ручну прописувати це

    return f"{session['data']}"


if __name__ == "__main__":
    app.run(debug=True)