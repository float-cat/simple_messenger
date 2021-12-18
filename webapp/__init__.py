from flask import Flask
from flask_login import LoginManager
from webapp.MODEL import db, User


from webapp.modules.IndexPage import IndexPage
from webapp.modules.MessagesPage import MessagesPage
from webapp.modules.AuthPage import AuthPage
from webapp.modules.RegisterPage import RegisterPage
from webapp.modules.LogoutPage import LogoutPage
from webapp.modules.NewGroupMessagesPage import NewGroupMessagesPage
from webapp.handlers.MessagesHandler import MessagesHandler
from webapp.handlers.SearchUsersHandler import SearchUsersHandler
from webapp.handlers.RegisterHandler import RegisterHandler
from webapp.handlers.AuthHandler import AuthHandler


def create_app():
    # Инициализация Flask приложения, config файла и базы данных
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)

    # Инициализация объекта авторизации
    Login_manager = LoginManager()
    Login_manager.init_app(app)
    Login_manager.login_view = 'auth'

    @Login_manager.user_loader
    def load_user(id):
        return User.query.get(id)


    # Главная страница
    @app.route('/')
    def index():
        return IndexPage()

    # Страница для отправки и получения сообщений
    @app.route('/messages')
    def messages():
        return MessagesPage()


    # Служебная страница обработчик формы сообщений по AJAX
    @app.route('/messagesproc', methods=['POST'])
    def process_messages():
        return MessagesHandler(db)

    
    # Служебная страница обработчик формы поиска пользователей по AJAX
    @app.route('/searchusersproc', methods=['POST'])
    def process_search():
        return SearchUsersHandler(db)


    # Страница авторизации
    @app.route('/auth')
    def auth():
        return AuthPage()

    # Страница регистрации
    @app.route('/register')
    def register():
        return RegisterPage()

    # Обработчик форм регистрации
    @app.route('/registerproc', methods=['POST'])
    def process_register():
        return RegisterHandler(db)

    # Обработчик формы авторизации
    @app.route('/authproc', methods=['POST'])
    def process_login():
        return AuthHandler()

    # Очистить куки, завершить сессию
    @app.route("/logout")
    def logout():
        return LogoutPage()

    return app
