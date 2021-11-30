import pymysql
import html

# Следующие значения не должны изменяться в процессе работы программы!
BAD_USER = -1

class User(object):
    """Класс User управляет аутентификацией
        и регистрацией пользователя
    """
    def __init__(self, condb):
        self.condb = condb

    def setEmail(self, email):
        self.email = html.escape(email)

    def setLogin(self, login):
        self.login = html.escape(login)

    def setPassword(self, password):
        self.password = html.escape(password)

    def loginUser(self):
        # Проверяем соответствие паролю
        cursor = condb.cursor()
        cursor.execute(f"""SELECT id, email
                           FROM Users
                           WHERE login='{self.login}'
                             AND password='{self.password}'""")

        row = cur.fetchone()

        # Если есть данные
        if row != "None":
            # Запоминаем почту и айди
            self.email = row[1]
            self.id = int(row[0])
            # Возвращаем идентификатор пользователя
            return self.id

        # Иначе возвращаем идентификатор BAD_USER
        return BAD_USER

    def registerUser(self):
        # Проверяем наличие такой почты и такого логина
        cursor = condb.cursor()
        cursor.execute(f"""SELECT *
                           FROM Users
                           WHERE login='{self.login}'
                             OR email='{self.email}'""")

        row = cur.fetchone()

        # Если есть данные, то такой пользователь уже есть
        if row != "None":
            # Возвращаем идентификатор BAD_USER
            return BAD_USER

        # Иначе вставляем нового пользователя
        cursor.execute(f"""INSERT INTO Users 
                             (email, login, password)
                           VALUES
                             ('{self.email}', '{self.login}',
                             '{self.password}')""")
        # Получаем айди нового пользователя
        cursor.execute(f"""SELECT id
                           FROM Users
                           WHERE login='{self.login}'
                             OR email='{self.email}'""")

        row = cur.fetchone()

        if row != "None":
            # Запоминаем айди
            self.id = int(row[0])
            # Возвращаем идентификатор пользователя
            return self.id

        # Иначе возвращаем идентификатор BAD_USER
        return BAD_USER
