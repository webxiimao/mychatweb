#-*- coding=utf8 -*-
'''
write by xii
'''
from flask_socketio import SocketIO,join_room,leave_room


socketio = SocketIO()


@socketio.on('connect')
def client_connect():
    socketio.emit('client_connect',{'data':"sucess"})



# 用户上线自动加入各有id的房间
@socketio.on('server_connent')
def server_connent(userInfo):
    room = userInfo['id']
    join_room(room)
    socketio.emit('client_connect',{'data':"success%s"%(userInfo['username'])},room=room)


#客户端发送消息
@socketio.on('send msg')
def send_msg(data):
    print(data)
    if 'src' in data.keys() :
        socketio.emit('client_get_msg', data, room=data['src'])
        socketio.emit('client_get_msg', data, room=data['des'])
    else:
        socketio.emit('client_get_msg', data)