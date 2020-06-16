import enum


class EnumTransactionType(enum.Enum):
    """
    Enum for transactions types
    """
    REQUIRED_NEW = "REQUIRED_NEW"
    PROPAGATED = "PROPAGATED"
    REQUIRED_NEVER = "REQUIRED_NEVER"
    PROPAGATED_CREATED = "PROPAGATED_CREATED"
