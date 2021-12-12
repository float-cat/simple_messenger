from flask import render_template, redirect, url_for, flash
from flask_login import current_user
from webapp.FORMS import simple_messenger_reg
from webapp.MODEL import User

def RegisterHandler(db):
    res = redirect(url_for('index'))
    form = simple_messenger_reg()
    if form.validate_on_submit():
        if User.query.filter(User.login == form.login.data).count():
            flash('Пользователь с таким логином уже существует')
            return redirect(url_for('register'))
        if User.query.filter(User.email == form.email.data).count():
            flash('Этот емаил уже зарегистрирован')
            return redirect(url_for('register'))
        new_user = User(login=form.login.data, email=form.email.data)
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Успешная регистрация. Теперь вы можете авторизоваться.')
        return res
    else:
        flash('Заполните все поля корректно')
        return redirect(url_for('register'))
