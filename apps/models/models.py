#-*- coding=utf8 -*-
'''
write by xii
'''

from chatapp import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    '''
    用户表
    '''
    id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    username = db.Column(db.String(56), nullable=False ,unique=True)
    password_hash = db.Column(db.String(128),nullable=False)
    nickname = db.Column(db.String(56), nullable=False)
    avater = db.Column(db.String(128))
    login_time = db.Column(db.Integer)

    def __init__(self, username, password):
        self.username = username
        self.password_hash = password

    def check_password(self,hash, password):
        return check_password_hash(hash, password)

    @staticmethod
    def set_password(password):
        return generate_password_hash(password)

    @staticmethod
    def add(user):
        db.session.add(user)
        return db.session.commit()

    def update(self):
        return db.session.commit()