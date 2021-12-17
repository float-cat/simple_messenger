from flask import request
from flask_login import current_user

from webapp.classes.SearchUsers import SearchUsers
from webapp.classes.Messages import Messages

def SearchUsersHandler(db):
    # Получаем данные формы
    typeRequest = request.form.get('typeRequest')
    userLogin = request.form.get('userLogin')
    # Проверяем аутентификацию пользователя
    if not current_user.is_authenticated:
        return 'Auth Fail!'
    # Если запрос на поиск
    if typeRequest == "search":
        # Создаем объект для работы с пользователями
        users = SearchUsers(db)
        # Выбираем пользователей
        result = users.getUsersByLogin(userLogin)
        return result
    elif typeRequest == "append":
        userId = request.form.get('userId')
        userId = userId[3:]      
        chatId = request.form.get('chatId')
        # Создаем объект для работы с сообщениями
        msg = Messages(db, str(current_user.id))
        # Добавляем пользователя в групповую переписку
        result = msg.appendToGroupChat(userId, chatId)
        return result
    return 'Fail!'
