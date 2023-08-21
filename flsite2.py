# Другий сайт, де вже є база даних, урок 8
import sqlite3
import os
from flask import Flask, render_template, request, g, flash, abort, redirect, url_for, make_response
from FDataBase import FDataBase
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from UserLogin import UserLogin
from forms import LoginForm, RegisterForm
from admin.admin import admin

# Конфігурація. Upper_letter - конфігураційна інформація

DATABASE = '/tmp/flsite.db'  # Шлях до бази даних
DEBUG = True
SECRET_KEY = 'ngjfsbgjuh87y78yds8gbdu'
MAX_CONTENT_LENGTH = 1024 * 1024  # Розмір в байтах

app = Flask(__name__)
app.config.from_object(__name__)  # завантажуємо конфіг з цього файлу
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'flsite.db')))  # Апдейтимо шлях до бд

app.register_blueprint(admin, url_prefix='/admin')  # Реєструємо наш blueprint admin

login_manager = LoginManager(app)
login_manager.login_view = 'login'  # Буде перенаправлення на login, якщо користувачу забронений доступ до сторінки
login_manager.login_message = "Авторизуйтеся для доступу до сторінки"
login_manager.login_message_category = "success"


@login_manager.user_loader
def load_user(user_id):
    print("load_user")
    return UserLogin().fromDB(user_id, dbase)


def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])  # Передаємо сетоду конект шлях до нашої бд
    conn.row_factory = sqlite3.Row  # Записи будуть не у вигляді кортежів, а у вигляді словника
    return conn


def create_db():  # Створюємо бд
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:  # читаємо файл sq_db.sql
        db.cursor().executescript(f.read())  # Запускаємо скріпти, які були прочитані в sq_db.sql
    db.commit()  # Записуємо зміни в базу даних
    db.close()


def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


dbase = None


@app.before_request
def before_request():
    global dbase
    db = get_db()
    dbase = FDataBase(db)


@app.route("/")
def index():
    return render_template('index.html', menu=dbase.getMenu(), posts=dbase.getPostsAnonce())


# Ця фукнція спрацює тоді, коли буде знищуватися контекст додатку. Це відбувається в момент закінчення обробки запиту
@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()


@app.route('/add_post', methods=["POST", "GET"])
def addPost():
    if request.method == "POST":
        if len(request.form['name']) > 4 and len(request.form['post']) > 10:
            res = dbase.addPost(request.form['name'], request.form['post'], request.form['url'])
            if not res:
                flash('Помилка додавання статті', category='error')
            else:
                flash('Стаття була добавлена', category='success')
        else:
            flash('Помилка додавання статті', category='error')

    return render_template('add_post.html', menu=dbase.getMenu(), title='Додавання статті')


@app.route("/post/<alias>")
@login_required
def showPost(alias):
    title, post = dbase.getPost(alias)
    if not title:
        abort(404)

    return render_template('post.html', menu=dbase.getMenu(), title=title, post=post)


@app.route("/login", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))

    form = LoginForm()
    if form.validate_on_submit():  # Перевіряємо чи були дані передані POST-запитом та перевіряє валідаці.
        user = dbase.getUserByEmail(form.email.data)
        if user and check_password_hash(user['psw'], form.psw.data):
            userlogin = UserLogin().create(user)
            rm = form.remember.data
            login_user(userlogin, remember=rm)
            return redirect(request.args.get("next") or url_for("profile"))
        else:
            flash("Неправильна пара логін/пароль", "error")
    return render_template("login.html", menu=dbase.getMenu(), title="Авторизація", form=form)


    # if request.method == "POST":
    #     user = dbase.getUserByEmail(request.form['email'])
    #     if user and check_password_hash(user['psw'], request.form['psw']):
    #         userlogin = UserLogin().create(user)
    #         rm = True if request.form.get('remainme') else False
    #         login_user(userlogin, remember=rm)
    #         return redirect(request.args.get("next") or url_for("profile"))
    #
    #     flash("Неправильна пара логін/пароль", "error")
    #
    # return render_template("login.html", menu=dbase.getMenu(), title='Авторизація')


@app.route("/register", methods=["POST", "GET"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hash = generate_password_hash(form.psw.data)
        res = dbase.addUser(form.name.data, form.email.data, hash)
        if res:
            flash("Ви успішно зареєструвались", 'success')
            return redirect(url_for('login'))
        else:
            flash("Помилка при додаванні в бд", "error")

    return render_template("register.html", menu=dbase.getMenu(), title='Реєстрація', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash("Ви вийшли з аккаунта", "success")
    return redirect(url_for('login'))


@app.route('/profile')
@login_required
def profile():
    return render_template("profile.html", menu=dbase.getMenu(), title='Профіль')


@app.route('/userava')
@login_required
def userava():
    img = current_user.get_avatar(app)
    if not img:
        return ""

    h = make_response(img)  # Створюємо об'єкт запиту
    h.headers['Content-Type'] = 'image/png'  # Вказуємо тип його контенту
    return h


@app.route('/upload', methods=["POST", "GET"])
@login_required
def upload():
    if request.method == "POST":
        file = request.files['file']
        if file and current_user.verifyExt(file.filename):
            try:
                img = file.read()
                res = dbase.updateUserAvatar(img, current_user.get_id())
                if not res:
                    flash("Помилка оновлення аватарку", "error")
                flash("Аватар було оновлено", "success")
            except FileNotFoundError as e:
                flash("Помилка читання файлу", "error")
        else:
            flash("Помилка оновлення аватара", "error")

    return redirect(url_for("profile"))


if __name__ == "__main__":
    app.run(debug=True)
