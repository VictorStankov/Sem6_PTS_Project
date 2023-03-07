import uuid
from application.user import User
from application.exceptions import DuplicateUserException


class Room:
    members = []

    def __init__(self):
        self.id = uuid.uuid4().hex[:10].upper()
        self.id = self.id[:5] + '-' + self.id[5:]

    def add_member(self, username: str):
        if username in [user.display_name for user in self.members]:
            raise DuplicateUserException()
        self.members.append(User(username))
