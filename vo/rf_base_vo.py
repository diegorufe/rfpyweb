"""

    Module for class base vo

"""
import json


class RFBaseVo:

    def __init__(self, table_name: str):
        """
        Class vo for dao
        :param table_name: for database
        """
        self.table_name = table_name
