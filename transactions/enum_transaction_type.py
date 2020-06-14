import enum


class EnumTransactionType(enum.Enum):
    """
    Enum for transactions types
    """
    REQUIRED_NEWS = "REQUIRED_NEWS"
    PROPAGATED = "PROPAGATED"
    REQUIRED_NEVER = "REQUIRED_NEVER"
