from flask import render_template, redirect, url_for, flash
from flask_login import current_user
from webapp.FORMS import simple_messenger_reg

def RegisterPage():
    title = "Регистрация"
    auth_forms = simple_messenger_reg()
    if current_user.is_authenticated:
        flash('Вы уже зарегистрированы')
        return redirect(url_for('index'))
    else:
        return render_template(
            'reg_user.html',
            page_title=title,
            form=auth_forms
        )
