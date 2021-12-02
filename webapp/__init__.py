from flask import Flask

from webapp.MODEL import db

from webapp.classes.Messages import Messages

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)

    @app.route('/')
    def index():
        return 'SimpleMessenger'
        
    @app.route('/test/')
    def test():
        msg = Messages(db, '1')
        msg.sendMessage('2', 'test !-_-!')
        return 'Test ok!';

    return app
