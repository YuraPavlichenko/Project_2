from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class LoginForm(FlaskForm):
    email = StringField("Email: ", validators=[Email("Пишеш херню")])
    psw = PasswordField("Password: ", validators=[DataRequired(), Length(min=4, max=100, message="Херня пароль")])
    remember = BooleanField("Remember me", default=False)
    submit = SubmitField("Увійти")

class RegisterForm(FlaskForm):
    name = StringField("Name: ", validators=[Length(min=4, max=100, message="Жопа цицьки проблема з іменем якщо що")])
    email = StringField("Email: ", validators=[Email("Пишеш херню, а не пошту")])
    psw = PasswordField("Password: ", validators=[DataRequired(), Length(min=4, max=100, message="Херня пароль")])
    psw2 = PasswordField("Password2: ", validators=[DataRequired(), EqualTo('psw', message="Сука неправильно")])
    submit = SubmitField("Реєстрація")