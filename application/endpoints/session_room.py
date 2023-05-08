from flask import request, render_template, session, url_for, redirect

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


@app.get('/join_room')
def join_room_get():
    room_code = request.args.get('room')
    if not isinstance(room_code, str) or not ScrumPoker.room_exists(room_code):
        return redirect(url_for('home_get'))
    return render_template('join.html', room_code=room_code)


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
