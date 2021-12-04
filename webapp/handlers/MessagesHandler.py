from flask import request

from webapp.classes.User import User, BAD_USER
from webapp.classes.Messages import Messages

def MessagesHandler(db):
    typeRequest = request.form.get('typeRequest')
    login = request.form.get('login')
    password = request.form.get('password')
    toUserId = request.form.get('toUserId')
    user = User(db, login, password)
    fromUserId = user.loginUser()
    if fromUserId == BAD_USER:
        return 'Auth Fail!'
    msg = Messages(db, str(fromUserId))
    if typeRequest == 'send':
        message = request.form.get('newMessageTmp')
        msg.sendMessage(str(toUserId), message)
        return 'Test ok! {}'.format(message)
    elif typeRequest == 'update':
        lastId = request.form.get('lastId')
        messages = msg.getMessagesDelta(lastId, str(toUserId))
        return messages
    return 'Test fail!'
