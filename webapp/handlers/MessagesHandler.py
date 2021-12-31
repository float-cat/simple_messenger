from flask import request
from flask_login import current_user

from webapp.classes.Messages import Messages

def MessagesHandler(db):
    # Получаем данные формы
    typeRequest = request.form.get('typeRequest')
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
    # Подгрузка предыдущих сообщений
    elif typeRequest == 'loadPrev':
        toUserId = request.form.get('toUserId')
        prevCount = request.form.get('prevCount')
        messages = msg.loadPrevMessages(toUserId, prevCount)
        return messages
    # Получение списка диалогов
    # DBG: Надо сделать так, чтобы отправлялись не все, а только новое!
    elif typeRequest == 'allPMInfo':
        isFull = int(request.form.get('isFull'))
        count = request.form.get('count')
        dialogs = msg.getAllPMInfo(isFull, count)
        return dialogs
    # Новая групповая переписка
    elif typeRequest == 'newGM':
        caption = request.form.get('caption')
        newIdInfo = msg.createNewGroupMessages(caption)
        return newIdInfo
    # Список пользователей в групповой переписке
    elif typeRequest == 'listusersofGM':
        chatId = request.form.get('chatId')
        newIdInfo = msg.getUsersInGroupMessages(chatId)
        return newIdInfo
    # Удаление пользователя из групповой переписки
    elif typeRequest == 'dropFromGM':
        chatId = request.form.get('chatId')
        userId = request.form.get('userId')
        newIdInfo = msg.dropFromGroupMessages(chatId, userId)
        return newIdInfo
    # Обновление заголовка переписки
    elif typeRequest == 'updateTitle':
        isPM = True
        pmId = request.form.get('userId')
        if not pmId:
            isPM = False            
            pmId = request.form.get('chatId')
        titleInfo = msg.updateTitleOfPM(pmId, isPM)
        return titleInfo
    # Блокировка пользователя
    elif typeRequest == 'blockUser':
        userId = request.form.get('userId')
        blockInfo = msg.blockUser(userId)
        return blockInfo
    return 'Request Fail!'
