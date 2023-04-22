import random
from string import ascii_uppercase
from typing import Dict

from application.model import Room

card_def = {
    'fib': [1, 2, 3, 5, 8, 13, 21, 40, 100],
    'powtwo': [1, 2, 4, 8, 16, 32, 64, 128],
    'others': [1, 2, 5, 10, 20, 50, 100]
}


class ScrumPoker:
    rooms: Dict[str, Room] = dict()

    @staticmethod
    def cards_exist(cards_key: str):
        return cards_key in card_def.keys()

    @classmethod
    def generate_unique_code(cls):
        while True:
            room_id = ''
            for i in range(10):
                room_id += random.choice(ascii_uppercase)
            if room_id[:5] + '-' + room_id[5:] not in cls.rooms:
                break
        return room_id[:5] + '-' + room_id[5:]

    @classmethod
    def add_room(cls, room_name: str, cards_key: str):
        room_code = cls.generate_unique_code()
        cls.rooms[room_code] = Room(room_name, room_code, card_def[cards_key])

        return cls.rooms[room_code]

    @classmethod
    def delete_room(cls, room_code: str):
        cls.rooms.pop(room_code)

    @classmethod
    def room_exists(cls, room_code: str):
        return room_code in cls.rooms.keys()

    @classmethod
    def get_room(cls, room_code: str):
        return cls.rooms[room_code]
