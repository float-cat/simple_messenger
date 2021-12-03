from flask import request
from webapp.classes.Messages import Messages

def MessagesHandler(db):
    typeRequest = request.form.get('typeRequest')
    # DBG Выполнение аутентификации пользователя
    msg = Messages(db, '1')
    if typeRequest == 'send':
        message = request.form.get('newMessageTmp')
        msg.sendMessage('2', message)
        return 'Test ok! {}'.format(message)
    elif typeRequest == 'update':
        lastId = request.form.get('lastId')
        messages = msg.getMessagesDelta(lastId, '2')
        return messages
    return 'Test fail!'
