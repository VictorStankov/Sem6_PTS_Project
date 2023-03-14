import random
from string import ascii_uppercase
from flask import request, render_template, session, url_for, redirect
from application import app, rooms

card_def = {
    'fib': [1, 2, 3, 5, 8, 13, 21, 40, 100],
    'powtwo': [1, 2, 4, 8, 16, 32, 64, 128],
    'others': [1, 2, 5, 10, 20, 50, 100]
}


def generate_unique_code():
    while True:
        room_id = ''
        for i in range(10):
            room_id += random.choice(ascii_uppercase)
        if room_id[:5] + '-' + room_id[5:] not in rooms:
            break
    return room_id[:5] + '-' + room_id[5:]


@app.get('/')
def home_get():
    return render_template(
        'home.html',
        error=session['error'] if 'error' in session.keys() else ''
    )


@app.post('/')
def home():
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
