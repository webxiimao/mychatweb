#-*- coding=utf8 -*-
'''
write by xii
'''
from apps.user.api import userApi


def register_blueprints(app):
    app.register_blueprint(userApi,url_prefix='/user')