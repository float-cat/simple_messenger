from flask import redirect, url_for, flash
from flask_login import logout_user

def LogoutPage():
    logout_user()
    flash('Вы успешно разлогинились')
    return redirect(url_for('index'))
