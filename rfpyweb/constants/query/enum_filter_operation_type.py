import enum


class EnumFilterOperationType(enum.Enum):
    """
    Enum for filter operation types
    """
    AND = "AND"
    OR = "OR"

    @staticmethod
    def convert(value: str):
        result = EnumFilterOperationType.AND

        if value == EnumFilterOperationType.OR:
            result = EnumFilterOperationType.OR

        return result
