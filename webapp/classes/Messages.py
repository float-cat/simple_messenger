import html
import sqlalchemy
import json

from sqlalchemy.orm import sessionmaker, scoped_session
from webapp.MODEL import db
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
        self.toUserId = html.escape(toUserId)        
        self.message = html.escape(message)
        today = datetime.datetime.now()
        self.session.execute(
            f"""INSERT INTO Messages
                  (fromUserId, toUserId, message, sendDate)
                VALUES ({self.fromUserId},
                  {self.toUserId}, '{self.message}', '{today}')""")
        self.session.commit()

    def getMessagesDelta(self, lastId, userId):
        lastId = html.escape(lastId)
        userId = html.escape(userId)
        result = self.session.execute(
            f"""SELECT Messages.id, login, message, sendDate, fromUserId
                FROM Users
                INNER JOIN Messages
                WHERE Messages.id > {lastId}
                  AND Users.id == Messages.fromUserId
                  AND (
                    Messages.fromUserId = {self.fromUserId}
                    OR Messages.toUserId = {self.fromUserId}
                  )
                  AND (
                    Messages.fromUserId = {userId}
                    OR Messages.toUserId = {userId}
                  )""")
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
            f"""SELECT fromUserId, login, Messages.id,
                    message, sendDate, fromUserId
                FROM Messages
                LEFT JOIN Users
                WHERE Users.id = fromUserId
                    AND toUserId = {self.fromUserId}
                    AND Messages.id IN (
                        SELECT MAX(id)
                        FROM Messages
                        WHERE toUserId = {self.fromUserId}
                        GROUP BY fromUserId
                    )
                UNION
                SELECT toUserId, login, Messages.id,
                    message, sendDate, fromUserId
                FROM Messages
                LEFT JOIN Users
                WHERE Users.id = toUserId
                    AND fromUserId = {self.fromUserId}
                    AND Messages.id IN (
                        SELECT MAX(id)
                        FROM Messages
                        WHERE fromUserId = {self.fromUserId}
                        GROUP BY toUserId
                    )""")
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
            # Если пользователя нет в списке или сообщение более новое
            if not (row[0] in resultDict) \
                or resultDict[row[0]]['messageid'] < int(row[2]):
                # Добавляем в спискок айди сообщения, если первый раз
                if not (row[0] in resultDict):
                    resultDict['msgids'][resultDict['count']] = int(row[0])
                    resultDict['count'] += 1
                # Запоминаем в словарь
                resultDict[row[0]] = {}
                resultDict[row[0]]['login'] = row[1]
                resultDict[row[0]]['messageid'] = int(row[2])
                if row[4]:
                    resultDict[row[0]]['time'] = self.formatTime(row[4])
                else:
                    resultDict[row[0]]['time'] = '--:--'
                if self.fromUserId == str(row[5]):
                    resultDict[row[0]]['message'] = 'Вы: ' + row[3]
                else:
                    resultDict[row[0]]['message'] = row[3]
        jsonString = json.dumps(resultDict)
        return jsonString
