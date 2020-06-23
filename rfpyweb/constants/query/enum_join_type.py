import enum
from rfpyutils.str.rf_utils_str import RFUtilsStr, LOW_BAR


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

    @staticmethod
    def convert(value: str):
        result = EnumJoinType.INNER_JOIN

        if value == EnumJoinType.INNER_JOIN or RFUtilsStr.replace(str(EnumJoinType.INNER_JOIN), LOW_BAR, " "):
            result = EnumJoinType.INNER_JOIN
        elif value == EnumJoinType.INNER_JOIN_FETCH or RFUtilsStr.replace(str(EnumJoinType.INNER_JOIN_FETCH), LOW_BAR,
                                                                          " "):
            result = EnumJoinType.INNER_JOIN_FETCH
        elif value == EnumJoinType.LEFT_JOIN or RFUtilsStr.replace(str(EnumJoinType.LEFT_JOIN), LOW_BAR, " "):
            result = EnumJoinType.LEFT_JOIN
        elif value == EnumJoinType.LEFT_JOIN_FETCH or RFUtilsStr.replace(str(EnumJoinType.LEFT_JOIN_FETCH), LOW_BAR,
                                                                         " "):
            result = EnumJoinType.LEFT_JOIN_FETCH
        elif value == EnumJoinType.RIGHT_JOIN or RFUtilsStr.replace(str(EnumJoinType.RIGHT_JOIN), LOW_BAR,
                                                                    " "):
            result = EnumJoinType.RIGHT_JOIN
        elif value == EnumJoinType.RIGHT_JOIN_FETCH or RFUtilsStr.replace(str(EnumJoinType.RIGHT_JOIN_FETCH), LOW_BAR,
                                                                          " "):
            result = EnumJoinType.RIGHT_JOIN_FETCH

        return result
