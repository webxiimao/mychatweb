#-*- coding=utf8 -*-
'''
write by xii
'''

class Config:
    SECRET_KEY="xiimao"
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@127.0.0.1:3306/mywechat'
    SQLALCHEMY_TRACK_MODIFICATIONS = True