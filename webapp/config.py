import os
from datetime import timedelta

'Динамический абсолютный путь к базе данных'
print(os.path.abspath(os.path.dirname(__file__)))
main_dir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(main_dir, '..', 'simple_messenger_database.db')}"

'seasurf токен (защита от кросс-скриптинга)'
SECRET_KEY='123132123sfdh234dfgj'

'Время жизни куки'
REMEMBER_COOKIE_DURATION = timedelta(days=15)