class ServerException(Exception):
    message: str
    http_status: int

    def __init__(self, message: str, http_status: int):
        super().__init__()

        self.message = message
        self.http_status = http_status


class DuplicateUserException(ServerException):
    def __init__(self):
        super().__init__('User with that name is already joined!', 401)
