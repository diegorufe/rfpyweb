"""

    Module for class base vo

"""
import json


class RFBaseVo:

    def __init__(self, table_name: str = None, pk_field='id'):
        """
        Class vo for dao
        :param table_name: for database
        :param pk_field: for table
        """
        self.table_name = table_name
        self.pk_field = pk_field
