from flask import request, render_template, session, url_for, redirect

from application import app, ScrumPoker


class JoinRoomEndpoints:
    @staticmethod
    @app.get('/join_room')
    def join_room_get():
        room_code = request.args.get('room')
        if not isinstance(room_code, str) or not ScrumPoker.room_exists(room_code):
            return redirect(url_for('home_get'))
        return render_template('join.html', room_code=room_code)

    @staticmethod
    @app.post('/join_room')
    def join_room_post():
        room_code = request.form.get('room_code')
        display_name = request.form.get('display_name')

        if not ScrumPoker.room_exists(room_code):
            session['error'] = 'Room not found'
            return redirect(url_for('home_get'))

        if not isinstance(display_name, str) or len(display_name) < 5:
            return render_template('join.html', error='Name too short', room_code=room_code)

        if ScrumPoker.get_room(room_code).member_exists(display_name):
            return render_template('join.html', error='User with that name has already joined', room_code=room_code)

        session['room_code'] = room_code
        session['display_name'] = display_name

        return redirect(url_for('get_room'))
