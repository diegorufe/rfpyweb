from constants.query.enum_filter_type import EnumFilterType
from constants.query.enum_filter_operation_type import EnumFilterOperationType


class Filter:

    def __init__(self, field: str = None, alias: str = None, filter_type=EnumFilterType.EQUAL, value=None,
                 filter_operation_type: EnumFilterOperationType = EnumFilterOperationType.AND, open_brackets: int = 1,
                 closed_brackets: int = 1):
        self.field = field
        self.alias = alias
        self.filter_type = filter_type
        self.value = value
        self.filter_operation_type = filter_operation_type
        self.open_brackets = open_brackets
        self.closed_brackets = closed_brackets
