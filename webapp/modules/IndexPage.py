from flask import render_template
from flask_login import current_user
def IndexPage():
    title = 'SimpleMessenger - главная страница'
    return render_template('index.html',
                           auth_validate=current_user.is_authenticated,
                           page_title=title)
