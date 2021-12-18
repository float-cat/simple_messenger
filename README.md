# Простой мессенджер Simple Messenger

## Цель
Написать простой мессенджер, позволяющий отправлять друг другу сообщения в режиме реального времени

## Задачи
* Спроектировать модель базы данных для мессенджера
* Разработать шаблон дизайна сайта
* Сделать аутентификацию пользователя
* Разработать обмен сообщениями между пользователями в режиме реального времени
  * Отправка сообщений
  * Прием сообщений
  * Получение списка всех последних сообщений
  * Создание групповой переписки
  * Добавление пользователей в групповую переписку
* Сделать простой поиск по всем пользователям
* Связать дизайн сайта с его логикой через шаблонизатор

## Скриншоты
![Переписка](https://sun9-67.userapi.com/impg/20yPKqatnGXpa2EB4gSFA5GkcFkdH6XTF4KY0A/MSqqZZybmSI.jpg?size=1366x768&quality=96&sign=bb1104449d265770ad3c2dcd9b225729&type=album)
![Переписка](https://sun9-15.userapi.com/impg/CiwzSiN7gGdKdfUPsBoIgMxb312FOom2aHwwzw/ZpAtcYSAgMw.jpg?size=1366x768&quality=96&sign=6c5aae966f5e9188557af25b21a922a2&type=album)

## Cтруктура проекта
```markdown
.
├── admin_createuser.py
├── create_db.py
├── dbscript
│   └── createdb.sql
├── README.md
├── requirements.txt
├── simple_messenger_database.db
├── test.txt
└── webapp
    ├── classes
    │   ├── Messages.py
    │   └── SearchUsers.py
    ├── config.py
    ├── FORMS.py
    ├── handlers
    │   ├── AuthHandler.py
    │   ├── MessagesHandler.py
    │   ├── RegisterHandler.py
    │   └── SearchUsersHandler.py
    ├── __init__.py
    ├── MODEL.py
    ├── modules
    │   ├── AuthPage.py
    │   ├── IndexPage.py
    │   ├── LogoutPage.py
    │   ├── MessagesPage.py
    │   ├── NewGroupMessagesPage.py
    │   └── RegisterPage.py
    ├── README.md
    ├── static
    │   ├── addsmile.js
    │   ├── css
    │   │   └── style.css
    │   ├── img
    │   │   └── background.png
    │   ├── IsMobile.js
    │   ├── MessagesAjax.js
    │   └── SearchUsersAjax.js
    └── templates
        ├── auth.html
        ├── base.html
        ├── index.html
        ├── messenger.html
        └── reg_user.html
```

## Прочее
В разработке, текущая актуальная ветка - stage
