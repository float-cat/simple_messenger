import html
import json

from sqlalchemy.orm import sessionmaker, scoped_session
import datetime

# Константы, не должны меняться
MAX_BLOCK_COUNT = 10

class Messages(object):
    """Класс Message управляет пересылкой сообщений
    """
    def __init__(self, db, fromUserId):
        self.db = db
        self.fromUserId = html.escape(fromUserId)
        engine = self.db.engine
        Session = scoped_session(sessionmaker(bind=engine))
        self.session = Session()

    def updateLastDate(self):
        today = datetime.datetime.now()
        result = self.session.execute(
            f"""UPDATE Users
                SET lastUpdate = '{today}'
                WHERE id = {self.fromUserId}"""
        )
        self.session.commit()

    def isGranted(self, chatId):
        result = self.session.execute(
            f"""SELECT userId
                FROM ChatUsers
                WHERE userId = {self.fromUserId}
                    AND chatid = {chatId}"""
        )
        row = result.fetchone()
        if row:
            return True
        return False

    def formatTime(self, timeString):
        rows = timeString.split('.')
        timeOfMessage = datetime.datetime.strptime(
            rows[0],
            "%Y-%m-%d %H:%M:%S"
        )
        today = datetime.datetime.today()
        if (today.toordinal() - timeOfMessage.toordinal()) > 0:
            return timeOfMessage.strftime("%d/%m/%Y")
        return timeOfMessage.strftime("%H:%M")

    def sendMessage(self, toUserId, message):
        isChat = False
        self.toUserId = html.escape(toUserId)        
        self.message = html.escape(message)
        if toUserId[0] == 'c':
            isChat = True
            self.toUserId = self.toUserId[1:]
        today = datetime.datetime.now()
        if isChat:
            self.session.execute(
                f"""INSERT INTO ChatMessages
                      (fromUserId, toChatId, message, sendDate)
                    VALUES ({self.fromUserId},
                      {int(self.toUserId)}, '{self.message}', '{today}')"""
            )
        else:
            self.session.execute(
                f"""INSERT INTO Messages
                      (fromUserId, toUserId, message, sendDate)
                    VALUES ({self.fromUserId},
                      {self.toUserId}, '{self.message}', '{today}')"""
            )
        self.session.commit()

    def getMessagesDelta(self, lastId, userId):
        prevCount = -1
        prevOffset = ''
        result = 0
        isChat = False
        lastId = html.escape(lastId)
        userId = html.escape(userId)
        if userId[0] == 'c':
            isChat = True
            userId = userId[1:]
            # Если нет доступа к групповому чату
            if not self.isGranted(userId):
                resultDict = {}                
                resultDict['error'] = 'Not Granted!'
                resultDict['lastid'] = 1
                jsonString = json.dumps(resultDict)
                return jsonString
        if isChat:
            # Признак первой загрузки - 0
            if int(lastId) == 0:
                # Получаем количество всех сообщений в этом чате
                result = self.session.execute(
                    f"""SELECT COUNT(*)
                        FROM ChatMessages
                        JOIN Users
                            ON fromUserId = Users.id
                        WHERE toChatId = {userId}"""
                )
                row = result.fetchone()
                countOfMessages = int(row[0])
                # Если сообщений больше чем в блоке
                if countOfMessages > MAX_BLOCK_COUNT:
                    # Оставляем сообщения, которые не влезли
                    prevCount = countOfMessages - MAX_BLOCK_COUNT
                else:
                    # Иначе предыдущих сообщений нет
                    prevCount = 0
                prevOffset = 'LIMIT ' + str(MAX_BLOCK_COUNT) + \
                    ' OFFSET ' + str(prevCount)
            result = self.session.execute(
                f"""SELECT ChatMessages.id, login, message, sendDate,
                        fromUserId
                    FROM ChatMessages
                    JOIN Users
                        ON fromUserId = Users.id
                    WHERE ChatMessages.id >  {lastId}
                        AND toChatId = {userId}
                    {prevOffset}
                    """
            )
        else:
            # Признак первой загрузки - -1
            if int(lastId) == 0:
                # Получаем количество всех сообщений в этом чате
                result = self.session.execute(
                    f"""SELECT COUNT(*)
                        FROM Users
                        JOIN Messages
                            ON Users.id == Messages.fromUserId
                        WHERE (
                                Messages.fromUserId = {self.fromUserId}
                                AND Messages.toUserId = {userId}
                            )
                            OR (
                                Messages.fromUserId = {userId}
                                AND Messages.toUserId = {self.fromUserId}
                            )"""
                )
                row = result.fetchone()
                countOfMessages = int(row[0])
                # Если сообщений больше чем в блоке
                if countOfMessages > MAX_BLOCK_COUNT:
                    # Оставляем сообщения, которые не влезли
                    prevCount = countOfMessages - MAX_BLOCK_COUNT
                else:
                    # Иначе предыдущих сообщений нет
                    prevCount = 0
                prevOffset = 'LIMIT ' + str(MAX_BLOCK_COUNT) + \
                    ' OFFSET ' + str(prevCount)
            result = self.session.execute(
                f"""SELECT Messages.id, login, message, sendDate, fromUserId
                    FROM Users
                    JOIN Messages
                        ON Users.id == Messages.fromUserId
                    WHERE Messages.id > {lastId}
                        AND ((
                                Messages.fromUserId = {self.fromUserId}
                                AND Messages.toUserId = {userId}
                            )
                            OR (
                                Messages.fromUserId = {userId}
                                AND Messages.toUserId = {self.fromUserId}
                            )
                        )
                    {prevOffset}"""
            )
        # DBG! Требуется рефакторинг
        # Объявляем словарь для формирования ответа
        #  Структура ответа
        #    {
        #        "lastid": <lastid>,
        #        "count": <count>,
        #        "msgids":
        #        {
        #            "0": <id1>
        #            ...
        #        },
        #        "id1":
        #        {
        #            "login": <login1>,
        #            "message": <message1>
        #            "time": <time1>
        #            "isOwner": <isOwner1>
        #        }
        #        ...
        #    }
        resultDict = {}
        resultDict['lastid'] = 0
        resultDict['count'] = 0
        resultDict['msgids'] = {}
        for row in result:
            resultDict['msgids'][resultDict['count']] = int(row[0])
            resultDict['count'] += 1
            resultDict[row[0]] = {}
            resultDict[row[0]]['login'] = row[1]
            resultDict[row[0]]['message'] = row[2]
            if row[3]:
                resultDict[row[0]]['time'] = self.formatTime(row[3])
            else:
                resultDict[row[0]]['time'] = '--:--'
            resultDict[row[0]]['isOwner'] = int(self.fromUserId == str(row[4]))
            lastId = str(row[0])
        resultDict['lastid'] = lastId
        if prevCount >= 0:
            resultDict['prevcount'] = prevCount
        jsonString = json.dumps(resultDict)
        return jsonString

    def loadPrevMessages(self, userId, prevCount):
        prevOffset = ''
        result = 0
        isChat = False
        prevCount = html.escape(prevCount)
        prevPrevCount = prevCount
        prevCount = int(prevCount) - MAX_BLOCK_COUNT
        if prevCount < 0:
            prevCount = 0
        userId = html.escape(userId)
        # Если признак группового чата
        if userId[0] == 'c':
            isChat = True
            userId = userId[1:]
            # Если нет доступа к групповому чату
            if not self.isGranted(userId):
                resultDict = {}                
                resultDict['error'] = 'Not Granted!'
                resultDict['prevcount'] = 0
                jsonString = json.dumps(resultDict)
                return jsonString
        if isChat:
            # Если осталось больше одного блока
            if int(prevCount) > 0:
                prevOffset = 'LIMIT ' + str(MAX_BLOCK_COUNT) + \
                    ' OFFSET ' + str(prevCount)
            # Иначе - последний блок
            else:
                prevOffset = 'LIMIT ' + str(prevPrevCount)
            result = self.session.execute(
                f"""SELECT ChatMessages.id, login, message, sendDate,
                        fromUserId
                    FROM ChatMessages
                    JOIN Users
                        ON fromUserId = Users.id
                    WHERE toChatId = {userId}
                    {prevOffset}
                    """
            )
        else:
            # Если осталось больше одного блока
            if int(prevCount) > 0:
                prevOffset = 'LIMIT ' + str(MAX_BLOCK_COUNT) + \
                    ' OFFSET ' + str(prevCount)
            # Иначе - последний блок
            else:
                prevOffset = 'LIMIT ' + str(prevPrevCount)
            result = self.session.execute(
                f"""SELECT Messages.id, login, message, sendDate, fromUserId
                    FROM Users
                    JOIN Messages
                        ON Users.id == Messages.fromUserId
                    WHERE (
                            Messages.fromUserId = {self.fromUserId}
                            AND Messages.toUserId = {userId}
                        )
                        OR (
                            Messages.fromUserId = {userId}
                            AND Messages.toUserId = {self.fromUserId}
                        )
                    {prevOffset}"""
            )
        # DBG! Требуется рефакторинг
        # Объявляем словарь для формирования ответа
        #  Структура ответа
        #    {
        #        "prevcount": <prevcount>,
        #        "count": <count>,
        #        "msgids":
        #        {
        #            "0": <id1>
        #            ...
        #        },
        #        "id1":
        #        {
        #            "login": <login1>,
        #            "message": <message1>
        #            "time": <time1>
        #            "isOwner": <isOwner1>
        #        }
        #        ...
        #    }
        resultDict = {}
        resultDict['count'] = 0
        resultDict['msgids'] = {}
        for row in result:
            resultDict['msgids'][resultDict['count']] = int(row[0])
            resultDict['count'] += 1
            resultDict[row[0]] = {}
            resultDict[row[0]]['login'] = row[1]
            resultDict[row[0]]['message'] = row[2]
            if row[3]:
                resultDict[row[0]]['time'] = self.formatTime(row[3])
            else:
                resultDict[row[0]]['time'] = '--:--'
            resultDict[row[0]]['isOwner'] = int(self.fromUserId == str(row[4]))
        resultDict['prevcount'] = prevCount
        jsonString = json.dumps(resultDict)
        return jsonString

    def getAllPMInfo(self, isFull, listCount):
        isPartQuery = ''
        if not isFull:
            isPartQuery = ' AND sendDate > lastUpdate'
        # Получаем последние сообщение в переписке с каждым пользователем
        result = self.session.execute(
            f"""SELECT fromUserId, login, login, Messages.id,
                    message, sendDate, fromUserId
                FROM Messages
                JOIN Users
                    ON Users.id = fromUserId
                WHERE toUserId = {self.fromUserId}
                    AND Messages.id IN (
                        SELECT MAX(id)
                        FROM Messages
                        WHERE toUserId = {self.fromUserId}
                        GROUP BY fromUserId
                    )
                    {isPartQuery}
                UNION
                SELECT toUserId, login, login, Messages.id,
                    message, sendDate, fromUserId
                FROM Messages
                JOIN Users
                    ON Users.id = toUserId
                WHERE fromUserId = {self.fromUserId}
                    AND Messages.id IN (
                        SELECT MAX(Messages.id)
                        FROM Messages
                        JOIN Users
                            ON Users.id = fromUserId
                        WHERE fromUserId = {self.fromUserId}
                            {isPartQuery}
                        GROUP BY toUserId
                    )
                UNION
                SELECT toChatId, caption, login,
                    ChatMessages.id, message, sendDate, fromUserId
                FROM ChatMessages
                JOIN Users
                    ON Users.id = fromUserId
                JOIN Chats
                    ON Chats.id = toChatId
                WHERE toChatId IN (
                        SELECT chatId 
                        FROM ChatUsers
                        WHERE userId = {self.fromUserId}
                    )
                    AND ChatMessages.id IN (
                        SELECT MAX(id)
                        FROM ChatMessages
                        GROUP BY toChatId
                    )                    
                    {isPartQuery}
                ORDER BY sendDate DESC
                LIMIT {listCount}"""
        )
        # Объявляем словарь для формирования ответа
        #  Структура ответа
        #    {
        #        "count": <count>,
        #        "msgids":
        #        {
        #            "0": <id1>
        #            ...
        #        },
        #        "id1":
        #        {
        #            "login": <login1>,
        #            "messageid": <messageid1>,
        #            "message": <message1>
        #            "time": <time1>
        #        }
        #        ...
        #    }
        resultDict = {}
        resultDict['count'] = 0
        resultDict['msgids'] = {}
        for row in result:
            # Запоминаем индекс
            idx = str(row[0])
            # Если пользователя нет в списке или сообщение более новое
            if not (idx in resultDict) \
                or resultDict[idx]['messageid'] < int(row[3]):
                # Добавляем в спискок айди сообщения, если первый раз
                #   если различаются название и логин - то это групповой чат
                if row[1] != row[2]:
                    idx = 'c' + idx
                if not (idx in resultDict):
                    resultDict['msgids'][resultDict['count']] = idx
                    resultDict['count'] += 1
                # Запоминаем в словарь
                resultDict[idx] = {}
                resultDict[idx]['login'] = row[1]
                resultDict[idx]['messageid'] = int(row[3])
                if row[5]:
                    resultDict[idx]['time'] = self.formatTime(row[5])
                else:
                    resultDict[idx]['time'] = '--:--'
                if self.fromUserId == str(row[6]):
                    resultDict[idx]['message'] = 'Вы: ' + row[4]
                elif row[1] != row[2]:
                    resultDict[idx]['message'] = row[2] + ': ' + row[4]
                else:
                    resultDict[idx]['message'] = row[4]
        if resultDict['count'] > 0:
            self.updateLastDate()
        if not isFull:
            resultDict['isnewmessages'] = 1
        else:
            resultDict['isnewmessages'] = 0
        jsonString = json.dumps(resultDict)
        return jsonString

    def appendToGroupChat(self, userId, chatId):
        userId = html.escape(userId)
        chatId = html.escape(chatId)
        # Проверяем является ли пользователь, который
        #  добавляет, создателем переписки
        result = self.session.execute(
            f"""SELECT ownerUserId
                FROM Chats
                WHERE ownerUserId = {self.fromUserId}
                    AND id = {chatId}"""
        )
        row = result.fetchone()
        if not row:
            return '{"status": "fail"}'
        # Проверяем добавлен ли уже пользователь в чат
        result = self.session.execute(
            f"""SELECT userId
                FROM ChatUsers
                WHERE userId = {userId}
                    AND chatid = {chatId}"""
        )
        row = result.fetchone()
        if row:
            return '{"status": "fail"}'
        # Добавляем пользователя в групповую переписку
        self.session.execute(
            f"""INSERT INTO ChatUsers (chatId, userId)
                VALUES ({chatId}, {userId})"""
        )
        self.session.commit()
        return '{"status": "ok"}'

    def createNewGroupMessages(self, caption):
        caption = html.escape(caption)
        if caption == "":
            caprion = "Новая переписка"
        # Добавляем групповую переписку
        self.session.execute(
            f"""INSERT INTO Chats (ownerUserId, caption)
                VALUES ({self.fromUserId}, '{caption}')"""
        )
        self.session.commit()
        # Получаем идентификатор новой переписки
        result = self.session.execute(
            f"""SELECT MAX(id)
                FROM Chats                
                WHERE ownerUserId = {self.fromUserId}
                GROUP BY ownerUserId"""
        )
        row = result.fetchone()
        if not row:
            return '{"newgm": 0}'
        chatId = row[0]
        # Добавляем создающего пользователя в групповую переписку
        self.session.execute(
            f"""INSERT INTO ChatUsers (chatId, userId)
                VALUES ({chatId}, {self.fromUserId})"""
        )
        self.session.commit()
        self.sendMessage('c' + str(chatId), 'Создал групповую переписку!')
        return '{"newgm": ' + str(chatId) + '}'

    def getUsersInGroupMessages(self, chatId):
        chatId = html.escape(chatId)
        # Проверяем есть ли пользователь в переписке
        result = self.session.execute(
            f"""SELECT userId, login
                FROM ChatUsers
                JOIN Users
                    ON userId = Users.id
                WHERE chatId = {chatId}
                    AND userId = {self.fromUserId}"""
        )
        row = result.fetchone()
        if not row:
            resultDict = {}
            resultDict['count'] = 0
            resultDict['msgids'] = {}
            jsonString = json.dumps(resultDict)
            return jsonString
        # Получаем список пользователей в переписке
        result = self.session.execute(
            f"""SELECT userId, login
                FROM ChatUsers
                JOIN Users
                    ON userId = Users.id
                WHERE chatId = {chatId}"""
        )
        # Объявляем словарь для формирования ответа
        #  Структура ответа
        #    {
        #        "count": <count>,
        #        "msgids":
        #        {
        #            "0": <id1>
        #            ...
        #        },
        #        "id1":
        #        {
        #            "login": <login1>
        #        },
        #        ...
        #        "isowner": <isownerstatus>
        #    }
        resultDict = {}
        resultDict['count'] = 0
        resultDict['msgids'] = {}
        for row in result:
            resultDict['msgids'][resultDict['count']] = int(row[0])
            resultDict['count'] += 1
            resultDict[row[0]] = {}
            resultDict[row[0]]['login'] = row[1]
        # Проверяем является ли пользователь владельцем переписки
        result = self.session.execute(
            f"""SELECT ownerUserId
                FROM Chats
                WHERE id = {chatId}
                    AND ownerUserId = {self.fromUserId}"""
        )
        row = result.fetchone()
        if not row:
            resultDict['isowner'] = 0
        else:
            resultDict['isowner'] = 1
        jsonString = json.dumps(resultDict)
        return jsonString

    def dropFromGroupMessages(self, chatId, userId):
        chatId = html.escape(chatId)
        userId = html.escape(userId)
        # Проверяем является ли пользователь владельцем переписки
        result = self.session.execute(
            f"""SELECT ownerUserId
                FROM Chats
                WHERE id = {chatId}
                    AND ownerUserId = {self.fromUserId}"""
        )
        row = result.fetchone()
        # Если не владелец или удаляет не сам себя
        if not row and userId != "-1":
            # Возвращаем статус фейл
            return '{"status": "fail"}'
        # Иначе - удаляем члена переписки
        dropUserId = userId
        if dropUserId == "-1":
            dropUserId = self.fromUserId
        result = self.session.execute(
            f"""DELETE FROM ChatUsers
                WHERE chatId = {chatId}
                    AND userId = {dropUserId}"""
        )
        self.session.commit()
        return '{"status": "ok"}'

