from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import builtins

# builtins.app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://USER:PASSWORD@localhost/SimpleMessenger'
builtins.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///c:/absolute/path/to/mysql.db'
db = SQLAlchemy(builtins.app)

# Таблица членов групповых переписок (связь много-ко-многим)
chat_users = db.Table('ChatUsers',
    db.Column('chatId', db.Integer, db.ForeignKey('Chats.id')),
    db.Column('userId', db.Integer, db.ForeignKey('Users.id'))
)

# Таблица банов пользователей (связь много-ко-многим)
block_users = db.Table('BlockUsers',
    db.Column('userId', db.Integer, db.ForeignKey('Users.id')),
    db.Column('blockUserId', db.Integer, db.ForeignKey('Users.id'))
)

# Таблица пользователей мессенджера
class User(db.Model):
    __tablename__ = 'Users'
    # Идентификатор пользователя
    id = db.Column(db.Integer(), primary_key=True, nullable=False)
    email = db.Column(db.String(60), unique=True, nullable=False)
    login = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(32), nullable=False)
    messages = db.relationship('Message', backref='user')
    chats = db.relationship('Chat', backref='user')
    chatUsers = db.relationship('Chat', secondary=chat_users, backref='user')
    chatMessages = db.relationship('ChatMessage', backref='user')
    blockUsers = db.relationship('User', secondary=block_users, backref='user')

# Таблица личных сообщений пользователей
class Message(db.Model):
    __tablename__ = 'Messages'
    # Уникальный идентификатор сообщения
    id = db.Column(db.Integer(), primary_key=True, nullable=False)
    # Отправитель сообщения
    fromUserId = db.Column(db.Integer(), db.ForeignKey('Users.id'))
    # Получатель сообщения
    toUserId = db.Column(db.Integer(), db.ForeignKey('Users.id'))
    # Сообщение
    message = db.Column(db.Text(), unique=True, nullable=False)
    # Время и дата отправки
    sendDate = db.Column(db.DateTime(), default=datetime.utcnow)

# Таблица групповых переписок
class Chat(db.Model):
    __tablename__ = 'Chats'
    # Уникальный идентификатор групповой переписки
    id = db.Column(db.Integer(), primary_key=True, nullable=False)
    # Создатель групповой переписки
    ownerUserId = db.Column(db.Integer(), db.ForeignKey('Users.id'))    
    chatMessages = db.relationship('ChatMessage', backref='chat')

# Таблица сообщений групповых переписок
class ChatMessage(db.Model):
    __tablename__ = 'ChatMessages'
    # Уникальный идентификатор сообщения групповой переписки
    id = db.Column(db.Integer(), primary_key=True, nullable=False)
    # Отправитель сообщения
    fromUserId = db.Column(db.Integer(), db.ForeignKey('Users.id'))
    # Идентификатор групповой переписки
    toChatId = db.Column(db.Integer(), db.ForeignKey('Chats.id'))
    # Сообщение
    message = db.Column(db.Text(), unique=True, nullable=False)
    # Время и дата отправления
    sendDate = db.Column(db.DateTime(), default=datetime.utcnow)

db.create_all()
