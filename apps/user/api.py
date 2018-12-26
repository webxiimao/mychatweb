#-*- coding=utf8 -*-
'''
write by xii
'''
from flask import Blueprint,request,jsonify
from apps.common import trueReturn,falseReturn
from apps.auth.auths import Auth
from apps.models.models import User
from sqlalchemy import or_
import time
import hashlib
import json

userApi = Blueprint('user',__name__)


@userApi.route('/register',methods=['POST'])
def register():
    '''
    注册
    :return:
    '''
    username = request.form.get('username')
    password = request.form.get('password')

    if username and password:
        if User.query.filter_by(username=username).first() is None:
            user = User(username,User.set_password(password))
            #md5加密生成随机头像
            hl = hashlib.md5()
            hl.update(username.encode(encoding='utf-8'))
            user.avater = "http://www.gravatar.com/avatar/%s?s=256&d=wavatar"%(hl.hexdigest())
            user.nickname = username
            result = User.add(user)
            returnUser = {
                'id':user.id,
                'username':user.username
            }
            return jsonify(trueReturn(returnUser, '用户注册成功'))
        return jsonify(falseReturn("", "该用户已存在", 700))
    return jsonify(falseReturn("", "用户名或密码不能为空", 700))



@userApi.route('/login',methods=['POST'])
def login():
    '''
    用户登录
    :return:
    '''
    username = request.form.get('username')
    password = request.form.get('password')

    if username and password:
        auth = Auth()
        return auth.authenticate(username, password)
    else:
        return jsonify(falseReturn("", "用户名或密码不能为空", 700))



@userApi.route("/info",methods=['POST'])
def info():
    '''
    从token获取用户信息
    :return:
    '''
    token = request.headers.get('weToken')
    if token:
        auth = Auth()
        result = auth.identification(token)
        if result['code'] == 200:
            return jsonify(trueReturn(result['data'],result['msg']))
        return jsonify(falseReturn("",result['msg'],result['code']))

    return jsonify(falseReturn("", "没有有效token", 902))



@userApi.route("/userSearch",methods=["GET"])
def userSearch():
    '''
    搜索注册用户
    :return:
    '''
    key_name = request.args.get('keyName')
    users = User.query.filter(or_(User.username.like("%"+ key_name +"%") if key_name else "", User.nickname.like("%"+ key_name +"%") if key_name else "")).all()
    json_users = []
    for user in users:
        json_user = {}
        (json_user['username'],) = user.username,
        (json_user['nickname'],) = user.nickname,
        (json_user['id'],) = user.id,
        (json_user['avater'],) = user.avater,
        json_users.append(json_user)

    return jsonify(trueReturn(json_users,"success"))
    # return json.dumps(users)

