from flask import session
from flask_socketio import join_room, leave_room, send

from application import socket_app, ScrumPoker


class SocketIOEndpoints:

    @staticmethod
    @socket_app.on('connect')
    def connect(auth):
        room_code = session.get('room_code')
        display_name = session.get('display_name')

        if not room_code or not display_name:
            return

        if not ScrumPoker.room_exists(room_code):
            leave_room(room_code)
            return

        join_room(room_code)
        send({'name': display_name, 'action': 'joined'}, to=room_code)
        ScrumPoker.get_room(room_code).add_member(display_name)
        print(f'{display_name} joined room {room_code}')

    @staticmethod
    @socket_app.on('disconnect')
    def disconnect():
        room_code = session.get('room_code')
        display_name = session.get('display_name')
        leave_room(room_code)

        if ScrumPoker.room_exists(room_code):
            room = ScrumPoker.get_room(room_code)
            room.remove_member(display_name)
            if len(room) <= 0:
                print('Deleting room: ', room_code)
                ScrumPoker.delete_room(room_code)

        send({'name': display_name, 'action': 'left'}, to=room_code)
        print(f'{display_name} has left the room {room_code}')
