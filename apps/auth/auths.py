#-*- coding=utf8 -*-
'''
write by xii
'''
import jwt,datetime,time
from flask import jsonify
from apps.models.models import User
from config import Config
from apps.common import trueReturn, falseReturn



class Auth(object):
    '''
    jwt权限管理模块
    '''
    @staticmethod
    def encode_auth_token(user_id,login_time):
        '''
        生成token
        :param user_id:
        :param login_time:
        :return:
        '''
        try:
            payload = {
                'exp':datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=10),
                'nbf':datetime.datetime.utcnow(),
                'iat':datetime.datetime.utcnow(),
                'iss':'mao',
                'data':{
                    'id':user_id,
                    'login_time':login_time
                }
            }
            return jwt.encode(payload, Config.SECRET_KEY, algorithm='HS256')

        except Exception as e:
            return e


    @staticmethod
    def decode_auth_token(token):
        try:
            payload = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'], options={'verify_exp': False})
            if 'data' in payload and 'id' in payload['data']:
                return payload
            else:
                raise jwt.InvalidTokenError
        except jwt.ExpiredSignatureError:
            return 'token已过期'
        except jwt.InvalidTokenError:
            return "token无效"
    # Signature has expired




    def authenticate(self, username, password):
        '''
        用户登录
        :param username:
        :param password:
        :return:
        '''
        userInfo = User.query.filter_by(username=username).first()
        if userInfo:
            if userInfo.check_password(userInfo.password_hash, password):
                user_id = userInfo.id
                login_time = int(time.time())
                userInfo.login_time = login_time
                userInfo.update()
                token = self.encode_auth_token(user_id, login_time)
                return jsonify(trueReturn(token.decode(), '登录成功'))
            return jsonify(falseReturn('','用户名或密码错误',900))
        return jsonify(falseReturn('','用户名不存在',700))



    def identification(self,token):
        '''
        用户鉴权
        :return:
        '''
        authsToken = token.split(" ")
        if (not authsToken) or (authsToken[0] != "JWT") or (len(authsToken) != 2):
            return falseReturn("","请传递正确的token头部信息", 902)
        else:
            payload = self.decode_auth_token(authsToken[1])

            if not isinstance(payload,str):
                user = User.query.filter_by(id=int(payload['data']['id'])).first()
                if user:
                    if user.login_time == payload['data']['login_time']:
                        userInfo = {
                            'id':user.id,
                            'username':user.username,
                            'avater':user.avater,
                            'nickname':user.nickname
                        }

                        return trueReturn(userInfo,"success")

                    return falseReturn("","该用户凭证已过期", 902)
                return falseReturn("","没有该用户的信息", 902)
            return falseReturn("",payload,902)
