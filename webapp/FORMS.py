from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, EmailField
from wtforms.validators import DataRequired, Email

'''Объект формы для авторизации'''

class simple_messenger_login(FlaskForm):
    login = StringField('Логин', validators=[DataRequired()], render_kw={"class": "form-control"})
    password = PasswordField('Пароль', validators=[DataRequired()], render_kw={"class": "form-control"})
    submit = SubmitField('Авторизация', render_kw={"class": "btn btn-primary"})
    checkbox = BooleanField('Запомнить меня', default=True, render_kw={"class": "form-check-input"})

class simple_messenger_reg(FlaskForm):
    login = StringField('Логин', validators=[DataRequired()], render_kw={"class": "form-control"})
    email = EmailField('Email', validators=[Email()], render_kw={"class": "form-control"})
    password = PasswordField('Пароль', validators=[DataRequired()], render_kw={"class": "form-control"})
    submit = SubmitField('Зарегистрироваться', render_kw={"class": "btn btn-primary"})

class simple_messenger_messages(FlaskForm):
    newMessage = StringField('Сообщение', validators=[DataRequired()], render_kw={"class": "form-control", "placeholder": "Введите сообщение"})
    submit = SubmitField('Отправить', render_kw={"class": "btn btn-primary main-send"})
    exit = SubmitField('Выход', render_kw={"class": "btn btn-light", "placeholder": "Введите сообщение"})

