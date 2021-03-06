"""
    Module for manage transactions for daos
"""
from rfpyweb.transactions.enum_transaction_type import EnumTransactionType
from rfpyweb.transactions.enum_db_engine_type import EnumDbEngineType
from pymysql.cursors import DictCursor


class RFTransaction:

    def __init__(self, enum_transaction_type: EnumTransactionType, transaction_database=None,
                 db_engine_type: EnumDbEngineType = EnumDbEngineType.RF_MYSQL_POOL):
        """
        Constructor for class transactions database
        :param enum_transaction_type:  type for transaction
        :param transaction_database:  is transaction database to apply
        :param db_engine_type: is db engine for transaction
        """
        self.enum_transaction_type = enum_transaction_type if not None else EnumTransactionType.PROPAGATED
        self.transaction_database = transaction_database
        self.db_engine_type = db_engine_type

    def execute_list_query(self, query, dic_params_query=None):
        """
        Method for execute list query
        :param query:
        :param dic_params_query:
        :return:
        """
        return self.execute_query(query, dic_params_query=dic_params_query, list_query=True)

    def execute_query(self, query, dic_params_query=None, list_query=False, insert=False, count=False):
        """
        Method for execute query
        :param query: to execute
        :param dic_params_query: for query
        :param list_query: is list query
        :param insert: is insert query
        :param count: count query
        :return: response for query
        """
        response = None

        if self.transaction_database is not None:
            if self.db_engine_type == EnumDbEngineType.RF_MYSQL_POOL or \
                    self.db_engine_type == EnumDbEngineType.RF_MYSQL:
                if list_query is True:
                    if self.db_engine_type == EnumDbEngineType.RF_MYSQL:
                        # No pool conection
                        cursor = self.transaction_database.cursor(cursor=DictCursor)
                    else:
                        cursor = self.transaction_database.cursor(dictionary=True)

                    cursor.execute(query, dic_params_query)
                    response = cursor.fetchall()
                elif count is True:
                    cursor = self.transaction_database.cursor()
                    cursor.execute(query, dic_params_query)
                    response = cursor.fetchall()
                    response = response[0][0]
                elif insert:
                    cursor = self.transaction_database.cursor()
                    cursor.execute(query, dic_params_query)
                    response = cursor.lastrowid
                else:
                    cursor = self.transaction_database.cursor()
                    response = cursor.execute(query, dic_params_query)

        return response
