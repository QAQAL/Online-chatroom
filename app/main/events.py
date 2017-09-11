from flask import session
from flask_socketio import (
    emit,
    join_room,
    leave_room,
)

from .. import socketio


@socketio.on('joined', namespace='/chat')
def joined(message):
    room = message['msg']
    join_room(room)
    session['room'] = room
    name = session.get('name')
    msg = '用户:({}) 进入了房间'.format(name)
    d = dict(
        msg=msg,
    )
    emit('status', d, room=room)


@socketio.on('xcxi', namespace='/chat')
def text(data):
    print("room", data.get("room"))
    room = data.get('room')
    name = session.get('name')
    msg = data.get('msg')
    d = dict(
        msg='{} : {}'.format(name, msg)
    )
    emit('message', d, room=room)


@socketio.on('left', namespace='/chat')
def left(message):
    room = session.pop('room')
    leave_room(room)
    name = session.get('name')
    d = dict(
        msg='{} 离开了房间'.format(name),
    )
    emit('status', d, room=room)
