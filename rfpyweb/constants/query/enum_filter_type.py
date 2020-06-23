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

    @staticmethod
    def convert(value: str):
        result = EnumFilterType.EQUAL

        if value == EnumFilterType.IN:
            result = EnumFilterType.IN
        elif value == EnumFilterType.LE:
            result = EnumFilterType.LE
        elif value == EnumFilterType.LT:
            result = EnumFilterType.LT
        elif value == EnumFilterType.GT:
            result = EnumFilterType.GT
        elif value == EnumFilterType.GE:
            result = EnumFilterType.GE
        elif value == EnumFilterType.NOT_IN:
            result = EnumFilterType.NOT_IN
        elif value == EnumFilterType.DISTINCT:
            result = EnumFilterType.DISTINCT

        return result
