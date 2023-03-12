import random
from string import ascii_uppercase
from secrets import token_bytes

from flask import Flask, request, render_template, session, url_for, redirect
from flask_socketio import join_room, leave_room, send, SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = token_bytes(64)
socketio = SocketIO(app)
rooms = {}


def generate_unique_code():
    while True:
        room_id = ''
        for i in range(10):
            room_id += random.choice(ascii_uppercase)
        if room_id[:5] + '-' + room_id[5:] not in rooms:
            break
    return room_id[:5] + '-' + room_id[5:]


@app.route('/', methods=['POST', 'GET'])
def home():
    card_def = {
        'fib': [1, 2, 3, 5, 8, 13, 21, 40, 100],
        'powtwo': [1, 2, 4, 8, 16, 32, 64, 128],
        'others': [1, 2, 5, 10, 20, 50, 100]
    }
    if request.method == 'POST':
        create_btn = request.form.get('create', False)
        join_btn = request.form.get('join', False)

        if join_btn is not False:
            display_name = request.form.get('display_name')
            room_code = request.form.get('room_code')

            if display_name == '':
                return render_template(
                    'home.html',
                    error='Please enter a name',
                    display_name=display_name, room_code=room_code
                )

            if room_code == '':
                return render_template(
                    'home.html',
                    error='Please enter a room code',
                    display_name=display_name, room_code=room_code
                )

            if room_code not in rooms:
                return render_template(
                    'home.html',
                    error='Room does not exist',
                    display_name=display_name, room_code=room_code
                )

            session['display_name'] = display_name
            session['room_code'] = room_code

        elif create_btn is not False:
            room_name = request.form.get('room_name')
            cards = request.form.get('cards')

            if room_name == '':
                return render_template(
                    'home.html',
                    error='Please enter a name',
                    room_name=room_name,
                    cards=cards
                )

            if cards not in card_def.keys():
                return render_template(
                    'home.html',
                    error='Incorrect card set!',
                    room_name=room_name,
                    cards=cards
                )

            room_code = generate_unique_code()
            rooms[room_code] = {'members': 0, 'name': room_name, 'cards': card_def[cards]}
            session['room_name'] = room_name
            session['room_code'] = room_code
            session['display_name'] = 'Host'
        else:
            return render_template('home.html')

        return redirect(url_for('room'))
    return render_template('home.html', error=session['error'] if 'error' in session.keys() else '')


@app.route('/room')
def room():
    room_code = session.get('room_code')
    display_name = session.get('display_name')
    if room_code is None or display_name is None or room_code not in rooms:
        return redirect(url_for('home'))

    room_name = rooms[room_code]['name']
    print(rooms, room_code, room_name, rooms[room_code])
    return render_template('room.html', room_name=room_name, cards=rooms[room_code]['cards'], room_code=room_code)


@app.route('/join_room', methods=['GET', 'POST'])
def join_room_extern():
    if request.method == 'GET':
        room_code = request.args.get('room')
        if not isinstance(room_code, str) or room_code not in rooms:
            return redirect(url_for('home'))
        return render_template('join.html', room_code=room_code)
    else:
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


@socketio.on('connect')
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
    rooms[room_code]['members'] += 1
    print(f'{display_name} joined room {room_code}')


@socketio.on('disconnect')
def disconnect():
    room_code = session.get('room_code')
    display_name = session.get('display_name')
    leave_room(room)

    if room_code in rooms:
        rooms[room_code]['members'] -= 1
        if rooms[room_code]['members'] <= 0:
            print('Deleting room: ', room_code)
            del rooms[room_code]

    send({'name': display_name, 'action': 'left'}, to=room_code)
    print(f'{display_name} has left the room {room_code}')


if __name__ == '__main__':
    socketio.run(app, debug=True)
