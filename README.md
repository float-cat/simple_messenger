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
* Сделать простой поиск по всем пользователям
* Связать дизайн сайта с его логикой через шаблонизатор

## Скриншот
![Переписка](https://sun9-29.userapi.com/impg/e3LXtXzvZox6b9ErzjW1-qmAhxCCSO8UDfrtuw/zyZCHqTxa0Y.jpg?size=1366x768&quality=96&sign=0d519d36c66def77472603bb6aedf222&type=album)

## Cтруктура проекта
```markdown
.
├── admin_createuser.py
├── create_db.py
├── dbscript
│   └── createdb.sql
├── README.md
├── requirements.txt
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
    │   └── RegisterPage.py
    ├── README.md
    ├── static
    │   ├── css
    │   │   └── style.css
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
