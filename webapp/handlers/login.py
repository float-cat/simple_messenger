#!/usr/bin/env python3
import cgi
from http import cookies
import datetime

sys.path.insert(0, "../classes")

from User import BAD_USER
from User import User

def setCookie(name, value):
    # Создаем куки
    c = cookies.SimpleCookie()
    # Определяем время
    time_to_live = datetime.timedelta(hours=1)
    expires = (datetime.datetime() + time_to_live)
    # Формат: Wdy, DD-Mon-YY HH:MM:SS GMT
    expires_at_time = expires.strftime('%a, %d %b %Y %H:%M:%S')
    c[name] = value
    c[name]['expires'] = expires_at_time 

def loginMain():
    form = cgi.FieldStorage()
    formType = form.getfirst("loginform", "None")
    login = form.getfirst("login", "None")
    password = form.getfirst("password", "None")    
    email = form.getfirst("email", "None")
    # Если тип формы не None значит у нас логин
    if formType != None:
        self.user = User(condb)
        # Устанавливаем атрибуты пользователя
        self.user.setLogin(login)
        self.user.setPassword(password)
        # Получаем айди пользователя
        userid = self.user.loginUser()
        # Если все прошло успешно
        if userid != BAD_USER:
            setCookie('login', login)
            setCookie('password', password)
    else
        # Проверяем есть ли форма register
        formType = form.getfirst("register", "None")
        # Если есть
        if formType != None:
            # Заполняем аттрибуты пользователя
            self.user.setLogin(login)
            self.user.setPassword(password)
            self.user.setEmail(email)
            # Регистрируем нового пользователя
            userid = self.user.registerUser()
            # Если вернулся нормальный айди
            if userid != BAD_USER:
                setCookie('login', login)
                setCookie('password', password)
