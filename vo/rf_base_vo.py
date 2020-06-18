"""

    Module for class base vo

"""


class RFBaseVo:
    # Table name for class
    __table_name__ = None
    # Dic columns for entity
    __dic_columns__ = {}
    # Pk for database
    __pk_field__ = None

    def __init__(self, table_name: str = None, pk_field='id'):
        """
        Class vo for dao
        :param table_name: for database
        :param pk_field: for table
        """
        self.table_name = table_name
        self.pk_field = pk_field
