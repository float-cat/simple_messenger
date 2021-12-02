import html
import sqlalchemy

from sqlalchemy.orm import sessionmaker, scoped_session
from webapp.MODEL import db
import datetime

class Messages(object):
    """Класс Message управляет пересылкой сообщений
    """
    def __init__(self, db, fromUserId):
        self.db = db
        self.fromUserId = html.escape(fromUserId)

    def sendMessage(self, toUserId, message):        
        self.toUserId = html.escape(toUserId)        
        self.message = html.escape(message)
        engine = self.db.engine
        Session = scoped_session(sessionmaker(bind=engine))

        s = Session()
        today = datetime.datetime.now()
        s.execute(f"INSERT INTO Messages \
            (fromUserId, toUserId, message, sendDate) \
            VALUES ({self.fromUserId}, \
            {self.toUserId}, '{self.message}', '{today}')")
        s.commit()
