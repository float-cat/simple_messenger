from flask import render_template, redirect, url_for, flash
from flask_login import login_user
from webapp.FORMS import simple_messenger_login
from webapp.MODEL import User

def AuthHandler():
    form = simple_messenger_login()
    # Если форма заполнена правильно, то обращаемся к базе данных
    if form.validate_on_submit():
        user = User.query.filter(User.login == form.login.data).first()
        """Если пользователь с логином найден в базе, то 
                 проверяем пароль на валидность.
                 для проверки хэширования после i использовать
                 User.check_password(form.passwod.data)"""
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.checkbox.data)
            flash('Идентификация и авторизация пройдена')
            return redirect(url_for('index'))
    flash('Что-то пошло не так')
    return redirect(url_for('auth'))
