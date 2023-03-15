from flask import session
from flask_socketio import join_room, leave_room, send

from application import socket_app, rooms


@socket_app.on('connect')
def connect(auth):
    room_code = session.get('room_code')
    display_name = session.get('display_name')

    if not room_code or not display_name:
        return

    if room_code not in rooms:
        leave_room(room_code)
        return

    join_room(room_code)
    send({'name': display_name, 'action': 'joined'}, to=room_code)
    rooms[room_code].add_member(display_name)
    print(f'{display_name} joined room {room_code}')


@socket_app.on('disconnect')
def disconnect():
    room_code = session.get('room_code')
    display_name = session.get('display_name')
    leave_room(room_code)

    if room_code in rooms:
        rooms[room_code].remove_member(display_name)
        if len(rooms[room_code]) <= 0:
            print('Deleting room: ', room_code)
            del rooms[room_code]

    send({'name': display_name, 'action': 'left'}, to=room_code)
    print(f'{display_name} has left the room {room_code}')
