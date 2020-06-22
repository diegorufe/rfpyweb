import enum


class EnumOrderType(enum.Enum):
    """
    Enum for order types
    """
    ASC = "ASC"
    DESC = "DESC"

    @staticmethod
    def convert(value: str):
        result = EnumOrderType.ASC

        if value == EnumOrderType.DESC:
            result = EnumOrderType.DESC

        return result
