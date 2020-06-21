import enum


class EnumFilterType(enum.Enum):
    """
    Enum for filter types
    """
    EQUAL = "EQUAL"
    IN = "IN"
    LE = "LE"
    LT = "LT"
    GT = "GT"
    GE = "GE"
    NOT_IN = "NOT_IN"
    DISTINCT = "DISTINCT"
