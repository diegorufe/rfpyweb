import enum


class EnumHttpStatusType(enum.Enum):
    """
    Enum http status
    """
    OK = 200
    CREATED = 201
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
