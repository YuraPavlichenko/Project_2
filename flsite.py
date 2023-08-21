from flask import Flask, render_template, url_for, request, flash, session, redirect, abort

app = Flask(__name__)  # Якщо вся програма пишеться в одному файлі, передаємо __name__
app.config['SECRET_KEY'] = 'fdsjnfksjiiii99'


menu = [{"name": "Елемент 1", "url": "element-1"},
        {"name": "Елемент 2", "url": "element-2"},
        {"name": "Елемент 3", "url": "element-3"},
        {"name": "Елемент 4", "url": "contact"}]


@app.route('/index')  # Вішаємо декілька url на 1 обробник
@app.route('/')
def hello():
    print(url_for('hello'))  # ulr_for повертає тільки перший url
    return render_template('index.html', title="Title з функції", menu=menu)  # Після першого параметру передаємо змінні


@app.route('/profile/<username>')
def profile(username):
    if 'userLogged' not in session or session['userLogged'] != username:
        abort(401)

    return f'Hello user {username}'


@app.route('/contact', methods=["POST", "GET"])
def contact():
    if request.method == "POST":
        if len(request.form['username']) > 2:
            flash('Дані відправлено', category='success')
        else:
            flash('Сталася помилка', category='error')
        print(request.form)

    return render_template('contact.html', menu=menu)


@app.route('/login', methods=["POST", "GET"])
def login():
    if 'userLogged' in session:
        return redirect(url_for('profile', username=session['userLogged']))
    elif request.method == 'POST' and request.form['username'] == '11' and request.form['psw'] == '11':
        session['userLogged'] = request.form['username']
        return redirect(url_for('profile', username=session['userLogged']))

    return render_template('login.html', title='Login', menu=menu)


@app.errorhandler(404)
def pageNotFound(error):
    return render_template('page404.html', title='Сторінку не знайдено', menu=menu)


if __name__ == "__main__":
    app.run(debug=True)
