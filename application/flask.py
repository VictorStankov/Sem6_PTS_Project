from secrets import token_bytes

from flask import Flask
from flask_qrcode import QRcode
from flask_socketio import SocketIO


app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.config['SECRET_KEY'] = token_bytes(64)
socket_app = SocketIO(app)
QRcode(app)
