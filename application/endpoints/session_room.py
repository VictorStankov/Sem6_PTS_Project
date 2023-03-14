from flask import request, render_template, session, url_for, redirect

from application import app, rooms


@app.get('/room')
def room():
    room_code = session.get('room_code')
    display_name = session.get('display_name')
    if room_code is None or display_name is None or room_code not in rooms:
        return redirect(url_for('home'))

    room_name = rooms[room_code]['name']
    return render_template(
        'room.html',
        room_name=room_name,
        cards=rooms[room_code]['cards'],
        room_code=room_code
    )


@app.get('/join_room')
def join_room_get():
    room_code = request.args.get('room')
    if not isinstance(room_code, str) or room_code not in rooms:
        return redirect(url_for('home'))
    return render_template('join.html', room_code=room_code)


@app.post('/join_room')
def join_room_post():
    room_code = request.form.get('room_code')
    display_name = request.form.get('display_name')

    if room_code not in rooms.keys():
        print(rooms, room_code)
        session['error'] = 'Room not found'
        return redirect(url_for('home'))

    if not isinstance(display_name, str) or len(display_name) < 5:
        return render_template('join.html', error='Name too short', room_code=room_code)
    session['room_code'] = room_code
    session['display_name'] = display_name

    return redirect(url_for('room'))
