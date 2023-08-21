from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'  # Об'явлємо вид бази даних та її місце розташування
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    psw = db.Column(db.String(500), nullable=True)  # Не може бути пустим
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"users - {self.id}"


class Profiles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=True)
    old = db.Column(db.Integer)
    city = db.Column(db.String(100))

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return f"users - {self.id}"


@app.route('/', methods=("POST", "GET"))
def index():
    return render_template("index2.html", title="Головна")


@app.route('/register', methods=("POST", "GET"))
def register():
    if request.method == "POST":
        try:
            hash = generate_password_hash(request.form['psw'])
            u = Users(email=request.form['email'], psw=hash)
            db.session.add(u)  # Додаємо в сесію, але не до таблиці в бд
            db.session.flush()  # Переносимо в бд, але поки що це все в памяті пристрою, таблиця буде така сама

            p = Profiles(name=request.form['name'], old=request.form['old'],
                         city=request.form['city'], user_id=u.id)
            db.session.add(p)
            db.session.commit()  # Уже кінцево міяємо все та додаємо в таблицю
        except:
            db.session.rollback()
            print("Помилка при додаванні в бд")

    return render_template("register2.html", title="Реєстрація")


if __name__ == "__main__":
    app.run(debug=True)