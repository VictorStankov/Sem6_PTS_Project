from flask import render_template, session, url_for, redirect

from application import app, ScrumPoker


class RoomEndpoints:
    @staticmethod
    @app.get('/room')
    def get_room():
        room_code = session.get('room_code')
        display_name = session.get('display_name')
        if room_code is None or display_name is None or not ScrumPoker.room_exists(room_code):
            return redirect(url_for('home_get'))

        room = ScrumPoker.get_room(room_code)

        return render_template(
            'room.html',
            room_name=room.room_name,
            cards=room.cards,
            room_code=room.room_code
        )
