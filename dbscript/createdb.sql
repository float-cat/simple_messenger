/**********************************
  Скрипт создания базы данных для
  мессенджера Simple Messenger
**********************************/

-- Создаем базу данных
CREATE DATABASE SimpleMessenger;

-- Переключаемся на созданную базу
USE SimpleMessenger;

-- Таблица пользователей мессенджера
CREATE TABLE Users (
    -- Уникальный идентификатор пользователя
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(60) UNIQUE NOT NULL,
    login NVARCHAR(20) UNIQUE NOT NULL,
    -- В поле пароля хранится хеш md5 пароля
    password VARCHAR(32) NOT NULL
    -- Время и дата последнего обновления
    lastUpdate DATE NOT NULL,
);

-- Таблица личных сообщений пользователей
CREATE TABLE Messages (
    -- Уникальный идентификатор сообщения
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    -- Отправитель сообщения
    fromUserId INT,
    -- Получатель сообщения
    toUserId INT,
    -- Сообщение
    message NVARCHAR(255) NOT NULL,
    -- Время и дата отправления
    sendDate DATE NOT NULL,
    -- Зависимость к первичному ключу пользователя
    FOREIGN KEY (fromUserId) REFERENCES Users(id),
    FOREIGN KEY (toUserId) REFERENCES Users(id)
);

-- Таблица групповых переписок
CREATE TABLE Chats (
    -- Уникальный идентификатор групповой переписки
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    -- Создатель групповой переписки
    ownerUserId INT NOT NULL,
    -- Название групповой переписки
    login NVARCHAR(60) NOT NULL,
    -- Зависимость к первичному ключу пользователя
    FOREIGN KEY (ownerUserId) REFERENCES Users(id)
);

-- Таблица членов групповых переписок (связь много-ко-многим)
CREATE TABLE ChatUsers (
    -- Идентификатор групповой переписки
    chatId INT NOT NULL,
    -- Идентификатор пользователя
    userId INT NOT NULL,
    -- Первичный ключ - пара связанных значений
    PRIMARY KEY (chatId, userId),
    -- Зависимость к первичному ключу групповой переписки
    FOREIGN KEY (chatId) REFERENCES Chats(id),
    -- Зависимость к первичному ключу пользователя
    FOREIGN KEY (userId) REFERENCES Users(id)
);

-- Таблица сообщений групповых переписок
CREATE TABLE ChatMessages (
    -- Уникальный идентификатор сообщения групповой переписки
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    -- Отправитель сообщения
    fromUserId INT NOT NULL,
    -- Идентификатор групповой переписки
    toChatId INT NOT NULL,
    -- Сообщение
    message NVARCHAR(255) NOT NULL,
    -- Время и дата отправления
    sendDate DATE NOT NULL,
    -- Зависимость к первичному ключу пользователя
    FOREIGN KEY (fromUserId) REFERENCES Users(id),
    -- Зависимость к первичному ключу групповой переписки
    FOREIGN KEY (toChatId) REFERENCES Chats(id)
);

-- Таблица банов пользователей (связь много-ко-многим)
CREATE TABLE BlockUsers (
    -- Идентификатор пользователя
    userId INT NOT NULL,
    -- Идентификатор забаненного пользователя
    blockUserId INT NOT NULL,
    -- Первичный ключ - пара связанных значений
    PRIMARY KEY (userId, blockUserId),
    -- Зависимость к первичному ключу пользователя
    FOREIGN KEY (userId) REFERENCES Users(id),
    FOREIGN KEY (blockUserId) REFERENCES Users(id)
);
