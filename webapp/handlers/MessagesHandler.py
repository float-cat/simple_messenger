from flask import request
from flask_login import current_user

from webapp.classes.Messages import Messages

def MessagesHandler(db):
    # Получаем данные формы
    typeRequest = request.form.get('typeRequest')
    login = request.form.get('login')
    password = request.form.get('password')
    toUserId = request.form.get('toUserId')
    # Проверяем аутентификацию пользователя
    if not current_user.is_authenticated:
        return 'Auth Fail!'
    fromUserId = current_user.id
    # Создаем объект для работы с сообщениями
    msg = Messages(db, str(fromUserId))
    # Отправка сообщения
    if typeRequest == 'send':
        message = request.form.get('newMessageTmp')
        msg.sendMessage(str(toUserId), message)
        return 'Test ok! {}'.format(message)
    # Получение новых сообщений
    elif typeRequest == 'update':
        lastId = request.form.get('lastId')
        messages = msg.getMessagesDelta(lastId, str(toUserId))
        return messages
    # Получение списка диалогов
    # DBG: Надо сделать так, чтобы отправлялись не все, а только новое!
    elif typeRequest == 'allPMInfo':
        dialogs = msg.getAllPMInfo()
        return dialogs
    return 'Request Fail!'
