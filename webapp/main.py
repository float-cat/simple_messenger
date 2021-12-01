from flask import Flask
import builtins

builtins.app = Flask(__name__)

import models.dbmodel

@app.route('/')
def index():
    return 'SimpleMessenger'

if __name__ == "__main__":
    builtins.app.run()
