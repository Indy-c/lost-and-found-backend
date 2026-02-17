from enum import Enum

class UserRole(str, Enum):
    OWNER = "OWNER"
    FINDER = "FINDER"
    ADMIN = "ADMIN"