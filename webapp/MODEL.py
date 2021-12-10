from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy()

# Таблица членов групповых переписок (связь много-ко-многим)
chat_users = db.Table('ChatUsers', db.metadata,
    db.Column('chatId', db.Integer, db.ForeignKey('Chats.id')),
    db.Column('userId', db.Integer, db.ForeignKey('Users.id'))
)

# Таблица банов пользователей (связь много-ко-многим)
block_users = db.Table('BlockUsers', db.metadata,
    db.Column('userId', db.Integer, db.ForeignKey('Users.id')),
    db.Column('blockUserId', db.Integer, db.ForeignKey('Users.id'))
)

# Таблица пользователей мессенджера
class User(db.Model, UserMixin):
    __tablename__ = 'Users'
    # Идентификатор пользователя
    id = db.Column(db.Integer(), primary_key=True, nullable=False)
    email = db.Column(db.String(60), unique=True, nullable=False)
    login = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    messages = db.relationship('Message',
        primaryjoin='User.id == Message.fromUserId or User.id == Message.toUserId',
        backref='user')
    chats = db.relationship('Chat',  primaryjoin='User.id == Chat.ownerUserId',
        backref='user')
    chatUsers = db.relationship('Chat', secondary=chat_users, backref='user')
    chatMessages = db.relationship('ChatMessage', 
        primaryjoin='User.id == ChatMessage.fromUserId', backref='user')
    blockUsers = db.relationship('User', secondary=block_users, backref='user')

    def __repr__(self):
        return 'Users {} {}'.format

    'Хэшируем пароль + проверка'
    def set_password(self, my_password):
        self.password = generate_password_hash(my_password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

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
    message = db.Column(db.Text(), nullable=False)
    # Время и дата отправки
    sendDate = db.Column(db.DateTime(), default=datetime.utcnow)

# Таблица групповых переписок
class Chat(db.Model):
    __tablename__ = 'Chats'
    # Уникальный идентификатор групповой переписки
    id = db.Column(db.Integer(), primary_key=True, nullable=False)
    # Создатель групповой переписки
    ownerUserId = db.Column(db.Integer(), db.ForeignKey('Users.id'))    
    chatMessages = db.relationship('ChatMessage',
        primaryjoin='Chat.id == ChatMessage.toChatId', backref='chat')

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
    message = db.Column(db.Text(), nullable=False)
    # Время и дата отправления
    sendDate = db.Column(db.DateTime(), default=datetime.utcnow)


