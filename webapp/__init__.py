from flask import Flask, request, render_template, redirect, url_for, flash, make_response
from flask_login import LoginManager, login_user, logout_user, current_user
from webapp.MODEL import db, User
from webapp.FORMS import simple_messenger_login

from webapp.modules.MessagesDiv import MessagesDiv
from webapp.handlers.MessagesHandler import MessagesHandler


def create_app():
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

    # Тестовая страница для отправки и получения сообщений
    @app.route('/messages')
    def messages():
        if current_user.is_authenticated:
            return MessagesDiv()
        else:
            flash('Авторизуйтесь пожалуйста')
            return redirect(url_for('auth'))



    # Служебная страница обработчик формы сообщений по AJAX
    @app.route('/messagesproc', methods=['POST'])
    def process_messages():
        return MessagesHandler(db)


    'Страница авторизации'
    @app.route('/auth')
    def auth():
        title = "Авторизация"
        auth_forms = simple_messenger_login()
        if current_user.is_authenticated:
            flash('Вы уже авторизованы')
            return redirect(url_for('index'))
        else:
            return render_template('auth.html', page_title=title, form=auth_forms)


    'обработчик формы авторизации'
    @app.route('/authproc', methods=['POST'])
    def process_login():
        res = redirect(url_for('index'))
        form = simple_messenger_login()
        'Если форма заполнена правильно, то обращаемся к базе данных'
        if form.validate_on_submit():
            user = User.query.filter(User.login == form.login.data).first()
            """Если пользователь с логином найден в базе, то 
                 проверяем пароль на валидность.
                 для проверки хэширования после i использовать
                 User.check_password(form.passwod.data)"""
            if user and user.check_password(form.password.data):
                login_user(user)
                # Устанавливаем куки на сроком на 15 дней
                if not request.cookies.get("login") \
                    or not request.cookies.get("password"):
                    # Создаем объект работающий с куками
                    res = make_response("Setting a cookie")
                    res.set_cookie("login", form.login.data,
                        max_age=60*60*24*15)
                    res.set_cookie("password", form.password.data,
                        max_age=60*60*24*15)
                flash('Идентификация и авторизация пройдена')
                return res

        flash('Что-то пошло не так')
        return res# redirect(url_for('index'))

    'Очистить куки, завершить сессию'
    @app.route("/logout")
    def logout():
        logout_user()
        flash('Вы успешно разлогинились')
        return redirect(url_for('index'))

    return app
