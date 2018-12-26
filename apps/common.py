#-*- coding=utf8 -*-
'''
write by xii
'''
def trueReturn(data, msg, code=200):
    return {
        'code':code,
        'data':data,
        'msg':msg

    }


def falseReturn(data, msg, code):
    return {
        "code": code,
        "data": data,
        "msg": msg
    }

