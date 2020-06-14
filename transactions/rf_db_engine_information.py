from transactions.enum_db_engine_type import EnumDbEngineType


class RFDbEngineInformation:

    def __init__(self, db_engine_type: EnumDbEngineType):
        """
        Constructor for class RFDbEngineInformation
        :param db_engine_type:
        """
        self.db_engine_type = db_engine_type
        self.dic_table_columns = {}
