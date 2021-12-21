from flask import render_template, redirect, url_for, flash
from flask_login import current_user
from webapp.FORMS import simple_messenger_login

def AuthPage():
    title = "Авторизация"
    # Создаем форму для ввода данных аутентификации
    auth_forms = simple_messenger_login()
    if current_user.is_authenticated:
        flash('Вы уже авторизованы')
        return redirect(url_for('index'))
    else:
        return render_template(
            'auth.html',
            uth_validate=current_user.is_authenticated,
            page_title=title,
            form=auth_forms
        )
