import enum


class EnumJoinType(enum.Enum):
    """
    Enum for join types
    """
    LEFT_JOIN = "LEFT_JOIN"
    INNER_JOIN = "INNER_JOIN"
    RIGHT_JOIN = "RIGHT_JOIN"
    LEFT_JOIN_FETCH = "LEFT_JOIN_FETCH"
    INNER_JOIN_FETCH = "INNER_JOIN_FETCH"
    RIGHT_JOIN_FETCH = "RIGHT_JOIN_FETCH"
