import html
import sqlalchemy
from sqlalchemy.orm import sessionmaker, scoped_session
from werkzeug.security import generate_password_hash, check_password_hash

from webapp.MODEL import db

# Следующие значения не должны изменяться в процессе работы программы!
BAD_USER = -1

class User(object):
    """Класс User управляет аутентификацией
        и регистрацией пользователя
        Используется для аутентификации 
        обработчика AJAX
    """
    def __init__(self, db, login, password):
        self.db = db
        self.login = html.escape(login)
        self.password = password
        engine = self.db.engine
        Session = scoped_session(sessionmaker(bind=engine))
        self.session = Session()

    def setEmail(self, email):
        self.email = html.escape(email)

    def getId(self):
        return self.id

    def getLogin(self):
        return self.login

    def getEmail(self):
        return self.email

    def loginUser(self):
        # Проверяем соответствие паролю
        result = self.session.execute(
            f"""SELECT id, email, password
                FROM Users
                WHERE login='{self.login}'""")
        row = result.fetchone()
        # Если есть данные
        if row:
            # Проверяем пароль
            if check_password_hash(row[2], self.password):
                # Запоминаем почту и айди
                self.email = row[1]
                self.id = int(row[0])
                # Возвращаем идентификатор пользователя
                return self.id

        # Такого пользователя нет, или пароль неверен
        return BAD_USER

    def registerUser(self):
        # Проверяем наличие такой почты и такого логина
        result = self.session.execute(
            f"""SELECT *
                FROM Users
                WHERE login='{self.login}'
                  OR email='{self.email}'""")
        row = result.fetchone()
        # Если есть данные, то такой пользовтель уже есть
        if row:
            # Возвращаем идентификатор BAD_USER
            return BAD_USER
        # Иначе вставляем нового пользователя
        password = generate_password_hash(self.password)
        self.session.execute(
            f"""INSERT INTO Users 
                  (email, login, password)
                VALUES
                  ('{self.email}', '{self.login}',
                    '{password}')""")
        # Получаем айди нового пользователя
        result = self.session.execute(
            f"""SELECT id
                FROM Users
                WHERE login='{self.login}'
                  OR email='{self.email}'""")
        row = result.fetchone()
        # Если есть данные
        if row:
            # Запоминаем айди
            self.id = int(row[0])
            # Возвращаем идентификатор пользователя
            return self.id
        # Иначе возвращаем идентификатор BAD_USER
        return BAD_USER
