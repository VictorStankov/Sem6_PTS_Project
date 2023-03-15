from secrets import token_bytes
from typing import Dict

from flask import Flask
from flask_qrcode import QRcode
from flask_socketio import SocketIO

from application.model import Room

rooms: Dict[str, Room] = dict()

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.config['SECRET_KEY'] = token_bytes(64)
socket_app = SocketIO(app)
QRcode(app)
