import html
import json

from sqlalchemy.orm import sessionmaker, scoped_session
import datetime

class Messages(object):
    """Класс Message управляет пересылкой сообщений
    """
    def __init__(self, db, fromUserId):
        self.db = db
        self.fromUserId = html.escape(fromUserId)
        engine = self.db.engine
        Session = scoped_session(sessionmaker(bind=engine))
        self.session = Session()

    def granted(self, chatId):
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
        result = 0
        isChat = False
        lastId = html.escape(lastId)
        userId = html.escape(userId)
        if userId[0] == 'c':
            isChat = True
            userId = userId[1:]
            # Если нет доступа к групповому чату
            if not self.granted(userId):
                resultDict = {}                
                resultDict['error'] = 'Not Granted!'
                resultDict['lastid'] = 1
                jsonString = json.dumps(resultDict)
                return jsonString
        if isChat:
            result = self.session.execute(
                f"""SELECT ChatMessages.id, login, message, sendDate,
                        fromUserId
                    FROM ChatMessages
                    JOIN Users
                        ON fromUserId = Users.id
                    WHERE ChatMessages.id >  {lastId}
                        AND toChatId = {userId}"""
            )
        else:
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
                        )"""
            )
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
        jsonString = json.dumps(resultDict)
        return jsonString

    def getAllPMInfo(self):
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
                UNION
                SELECT toUserId, login, login, Messages.id,
                    message, sendDate, fromUserId
                FROM Messages
                JOIN Users
                    ON Users.id = toUserId
                WHERE fromUserId = {self.fromUserId}
                    AND Messages.id IN (
                        SELECT MAX(id)
                        FROM Messages
                        WHERE fromUserId = {self.fromUserId}
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
                    )"""
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
        jsonString = json.dumps(resultDict)
        return jsonString
