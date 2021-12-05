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
        textplain = ""   
        lastId = html.escape(lastId)
        userId = html.escape(userId)
        result = self.session.execute(
            f"""SELECT Messages.id, login, message
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
        for row in result:
            textplain += f"""{row[1]}: {row[2]}\n"""
            lastId = str(row[0])
        textplain = lastId + "|" + textplain
        return textplain

    def getAllPMInfo(self):
        jsonString = ""
        # Получаем последние сообщение в переписке с каждым пользователем
        result = self.session.execute(
            f"""SELECT fromUserId, login, Messages.id,
                    message
                FROM Messages
                LEFT JOIN Users
                WHERE Users.id = fromUserId
                    AND toUserId = {self.fromUserId}
                    AND Messages.id IN (
                        SELECT MAX(id)
                        FROM Messages
                        GROUP BY fromUserId
                    )
                UNION
                SELECT toUserId, login, Messages.id,
                    message
                FROM Messages
                LEFT JOIN Users
                WHERE Users.id = toUserId
                    AND fromUserId = {self.fromUserId}
                    AND Messages.id IN (
                        SELECT MAX(id)
                        FROM Messages
                        GROUP BY toUserId
                    )""")
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
                resultDict[row[0]]['message'] = row[3]
        jsonString = json.dumps(resultDict)
        return jsonString
