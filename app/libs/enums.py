from enum import Enum

class UserStatusEnum(Enum):
    ACTIVE = 1
    NO_ACTIVE = 0


class UserPermissionEnum(Enum):
    ADMIN = 1
    USER  = 0
