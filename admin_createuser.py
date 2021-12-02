import sys

from webapp import create_app
from webapp.MODEL import db, User

'Используем контекст веб приложения'
app = create_app()

with app.app_context():

    login = input('Введите логин: ')
    'Проверка на наличие логина в базе'
    if User.query.filter(User.login == login).count():
        print('Пользователь с таким логином уже существует')
        sys.exit()

    email = input('Введите email: ')
    'Проверка уже зарегистрированного email'
    if User.query.filter(User.email == email).count():
        print('Этот емаил уже зарегистрирован')
        sys.exit()

    password = input('Введите пароль')

    'Создаем нового пользователя в User'
    new_user = User(login=login, email=email)
    new_user = User.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    print('Пользователь id {} создан и добавлен в базу данных'.format(new_user.id))

