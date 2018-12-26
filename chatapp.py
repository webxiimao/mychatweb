#-*- coding=utf8 -*-
'''
write by xii
'''
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import *
from config import Config



app = Flask(__name__)
app.config['SECRET_KEY'] = Config.SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = Config.SQLALCHEMY_TRACK_MODIFICATIONS

CORS(app, supports_credentials=True)

db = SQLAlchemy(app)
migrate = Migrate(app,db)

from apps.socketapi.event import socketio
from apps import register_blueprints

register_blueprints(app)

socketio.init_app(app)


if __name__ == "__main__":
    socketio.run(app)
