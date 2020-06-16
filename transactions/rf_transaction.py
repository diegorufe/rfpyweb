"""
    Module for manage transactions for daos
"""
from transactions.enum_transaction_type import EnumTransactionType
from transactions.enum_db_engine_type import EnumDbEngineType
from pymysql.cursors import DictCursor


class RFTransaction:

    def __init__(self, enum_transaction_type: EnumTransactionType, transaction_database=None,
                 db_engine_type: EnumDbEngineType = EnumDbEngineType.RF_MYSQL):
        """
        Constructor for class transactions database
        :param enum_transaction_type:  type for transaction
        :param transaction_database:  is transaction database to apply
        :param db_engine_type: is db engine for transaction
        """
        self.enum_transaction_type = enum_transaction_type if not None else EnumTransactionType.PROPAGATED
        self.transaction_database = transaction_database
        self.db_engine_type = db_engine_type

    def execute_list_query(self, query, dic_params=None):
        """
        Method for execute list query
        :param query:
        :param dic_params:
        :return:
        """
        return self.__execute_query__(query, dic_params=dic_params, list_query=True)

    def __execute_query__(self, query, dic_params=None, list_query=False):
        """
        Method for execute query
        :param query: to execute
        :param dic_params: for query
        :param list_query: is list query
        :return: response for query
        """
        response = None

        if self.transaction_database is not None:
            if self.db_engine_type == EnumDbEngineType.RF_MYSQL:
                if list_query is True:
                    cursor = self.transaction_database.cursor(cursor=DictCursor)
                else:
                    cursor = self.transaction_database.cursor()

                response = cursor.execute(query, dic_params)

        return response
