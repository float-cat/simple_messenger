import html
import sqlalchemy
import json

from sqlalchemy.orm import sessionmaker, scoped_session
from webapp.MODEL import db

class SearchUsers(object):
    """Класс SearchUsers ищет пользователей
    """
    def __init__(self, db):
        self.db = db
        engine = self.db.engine
        Session = scoped_session(sessionmaker(bind=engine))
        self.session = Session()

    def getUsersByLogin(self, userLogin):
        userLogin = html.escape(userLogin)
        result = self.session.execute(
            f"""SELECT id, login
                FROM Users
                WHERE login
                    LIKE '%{userLogin}%'
                LIMIT 50""")
        # Объявляем словарь для формирования ответа
        #  Структура ответа
        #    {
        #        "count": <count>,
        #        "msgids":
        #        {
        #            "0": <id1>
        #            ...
        #        },
        #        "id1": <login1>,
        #        ...
        #    }
        resultDict = {}
        resultDict['count'] = 0
        resultDict['msgids'] = {}
        for row in result:
            resultDict['msgids'][resultDict['count']] = int(row[0])
            resultDict['count'] += 1
            resultDict[row[0]] = row[1]
        jsonString = json.dumps(resultDict)
        return jsonString
