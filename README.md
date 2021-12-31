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
* Разработать загрузку сообщений и переписок через AJAX по событию прокрутки элементов страницы
* Сделать блокировку пользователей
* Связать дизайн сайта с его логикой через шаблонизатор

## Скриншоты
![Переписка](https://sun9-83.userapi.com/impg/zXsn8uIlxZhBlybrpykuLu0ZTLywfIkTiccrOA/R6Lcz9CIi3I.jpg?size=1280x720&quality=96&sign=517425bad1e9955462e192ffd6f5a60b&type=album)
![Переписка](https://sun9-80.userapi.com/impg/5yBhBhnvT57vIX32Snc7Gdba0G8nHRpRBapepQ/xUmJuvvdUkI.jpg?size=1280x720&quality=96&sign=da78ce229ddbc3d8b7d3e850eb30d46e&type=album)

## Cтруктура проекта
```markdown
.
├── admin_createuser.py
├── create_db.py
├── dbscript
│   └── createdb.sql
├── .gitignore
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
    │   ├── img
    │   │   ├── background.png
    │   │   └── favicon.ico
    │   └── js
    │       ├── IsMobile.js
    │       ├── MessagesAjax.js
    │       ├── SearchUsersAjax.js
    │       └── tooltipsSmile.js
    └── templates
        ├── auth.html
        ├── base.html
        ├── index.html
        ├── messenger.html
        └── reg_user.html
```

