import enum

class Role(enum.Enum):
    ADMIN = "admin"
    MODERATOR = "moderator"
    USER = "user"


class Answer(enum.Enum):
    A = "a"
    B = "b"
    C = "c"
    D = "d"