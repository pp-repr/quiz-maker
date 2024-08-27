import enum

class Role(enum.Enum):
    ADMIN = "admin"
    MODERATOR = "moderator"
    USER = "user"