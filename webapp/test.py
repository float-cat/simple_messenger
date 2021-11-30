#!/usr/bin/env python3

print("Content-type: text/html")
print()
print("""<html>
          <head>
           <meta charset="utf-8" />
           <title>
            Тестовый файл
           </title>
          </head>
          <body>
          <form name="loginform" method="POST" action="handler/login.py">
           <input name="login" type="text">
           </input>
           <input name="password" type="password">
           </input>
           <input type="submit" value="Войти">
           </input>
          </form>
          <form name="register" method="POST" action="handler/login.py">
           <input name="login" type="text">
           </input>
           <input name="email" type="text">
           </input>
           <input name="password" type="password">
           </input>
           <input type="submit" value="Регистрация">
           </input>
          </form>
          </body>
          </html>""")
