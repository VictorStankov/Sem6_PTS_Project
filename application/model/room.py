from typing import List

from application.model.user import User


class Room:
    _members: List[User] = []

    def __init__(self, room_name: str, room_code: str, cards: List[int]):
        self.room_name = room_name
        self.room_code = room_code
        self.cards = cards

    def __len__(self):
        return len(self._members)

    def add_member(self, username: str):
        self._members.append(User(username))

    def remove_member(self, username: str):
        for i in range(len(self._members)):
            if self._members[i].display_name == username:
                self._members.pop(i)

    def member_exists(self, username: str):
        return username in [user.display_name for user in self._members]
