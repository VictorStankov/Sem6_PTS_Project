from flask import request, render_template, session, url_for, redirect

from application import app, ScrumPoker


class HomeEndpoints:

    @staticmethod
    @app.get('/')
    def home_get():
        return render_template(
            'home.html',
            error=session['error'] if 'error' in session.keys() else ''
        )

    @staticmethod
    @app.post('/')
    def home_post():
        create_btn = request.form.get('create', False)
        join_btn = request.form.get('join', False)

        if create_btn is not False:
            room_name = request.form.get('room_name')
            cards = request.form.get('cards')

            if room_name == '':
                return render_template(
                    'home.html',
                    error='Please enter a name',
                    room_name=room_name,
                    cards=cards
                )

            if not ScrumPoker.cards_exist(cards):
                return render_template(
                    'home.html',
                    error='Incorrect card set!',
                    room_name=room_name,
                    cards=cards
                )

            room = ScrumPoker.add_room(room_name, cards)

            session['room_name'] = room.room_name
            session['room_code'] = room.room_code
            session['display_name'] = 'Host'

        elif join_btn is not False:
            display_name = request.form.get('display_name')
            room_code = request.form.get('room_code')

            if not isinstance(display_name, str) or display_name == '':
                return render_template(
                    'home.html',
                    error='Please enter a name',
                    room_code=room_code
                )

            if len(display_name) < 5:
                return render_template(
                    'home.html',
                    error='Name too short',
                    room_code=room_code
                )

            if not isinstance(room_code, str) or room_code == '':
                return render_template(
                    'home.html',
                    error='Please enter a room code',
                    display_name=display_name
                )

            if ScrumPoker.room_exists(room_code):
                return render_template(
                    'home.html',
                    error='Room does not exist',
                    display_name=display_name
                )

            if ScrumPoker.get_room(room_code).member_exists(display_name):
                return render_template(
                    'home.html',
                    error='User with that name has already joined'
                )

            session['display_name'] = display_name
            session['room_code'] = room_code
        else:
            return render_template('home.html')

    return redirect(url_for('room'))
