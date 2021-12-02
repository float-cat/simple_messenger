from flask import Flask, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_user

from webapp.MODEL import db, User
from webapp.FORMS import simple_messenger_login


'Инициализация Flask приложения, config файла и базы данных'
app = Flask(__name__)
app.config.from_pyfile('config.py')
db.init_app(app)

'Инициализация объекта авторизации'
Login_manager = LoginManager()
Login_manager.init_app(app)
Login_manager.login_view = 'auth'

@Login_manager.user_loader
def load_user(id):
    return User.query.get(id)


'Главная страница'
@app.route('/')
def index():
    title = 'SimpleMessenger - главная страница'
    return render_template('index.html', page_title=title)


'Страница авторизации'
@app.route('/auth')
def auth():
    title = "Авторизация"
    auth_forms = simple_messenger_login()
    return render_template('auth.html', page_title=title, form=auth_forms)


'обработчик формы авторизации'
@app.route('/authproc', methods=['POST'])
def process_login():
    form = simple_messenger_login()

    'Если форма заполнена правильно, то обращаемся к базе данных'
    if form.validate_on_submit():
        user = User.query.filter(User.login == form.login.data).first()
        """Если пользователь с логином найден в базе, то 
             проверяем пароль на валидность. для проверки хэширования после i использовать
             User.check_password(form.passwod.data)"""
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Идентификация и авторизация пройдена')
            return redirect(url_for('auth'))

    flash('Что-то пошло не так')
    return redirect(url_for('index'))
app.run()

