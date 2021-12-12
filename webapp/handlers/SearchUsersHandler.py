from flask import request
from flask_login import current_user

from webapp.classes.SearchUsers import SearchUsers

def SearchUsersHandler(db):
    # Получаем данные формы
    userLogin = request.form.get('userLogin')
    # Проверяем аутентификацию пользователя
    if not current_user.is_authenticated:
        return 'Auth Fail!'
    # Создаем объект для работы с пользователями
    users = SearchUsers(db)
    # Выбираем пользователей
    result = users.getUsersByLogin(userLogin)
    return result
