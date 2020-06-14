"""

 Class for manage transactions

"""
from transactions.enum_transaction_type import EnumTransactionType


class RFTransactionManager:

    def __init__(self, function_create_transaction=None, function_commit_transaction=None,
                 function_rollback_transaction=None):
        """
        Class for manage transactions
        :param function_create_transaction:
        :param function_commit_transaction:
        :param function_rollback_transaction:
        """
        self.function_create_transaction = function_create_transaction
        self.function_commit_transaction = function_commit_transaction
        self.function_rollback_transaction = function_rollback_transaction
        self.dic_information_db_engines = None

    def create_transaction(self, enum_transaction_type: EnumTransactionType = EnumTransactionType.PROPAGATED,
                           params=None):
        """
        Method for create transaction
        :param enum_transaction_type:  type for transaction to create
        :param params
        :return: response for transaction create
        """
        # set default transaction propagated
        enum_transaction_type = enum_transaction_type if not None else EnumTransactionType.PROPAGATED
        response = None
        if self.function_create_transaction is not None:
            response = self.function_create_transaction(enum_transaction_type, params=params)
        return response

    def commit(self, rf_transaction, params=None):
        """
        Method for commit transaction
        :param rf_transaction:
        :param params
        :return: response for commit transaction
        """
        response = None
        try:
            if rf_transaction is not None and self.function_commit_transaction is not None:
                response = self.function_commit_transaction(rf_transaction, params)
        except Exception as ex:
            response = self.rollback(rf_transaction, params=params)
        return response

    def rollback(self, rf_transaction, params=None):
        """
        Method for rollback transaction
        :param rf_transaction:  to rollback
        :param params
        :return: response for rollback transaction
        """
        response = None
        if rf_transaction is not None and self.function_rollback_transaction is not None:
            response = self.function_commit_transaction(rf_transaction, params=params)
        return response

    def get_fields_table(self, table_name, db_engine_type):
        """
        Method for get fields for table
        :param table_name: is a name for table to get columns
        :param db_engine_type:
        :return: ar columns if found esle return empty array
        """
        ar_fields = []

        if self.dic_information_db_engines is not None and db_engine_type is not None and table_name is not None and \
                db_engine_type in self.dic_information_db_engines:
            dic_table_columns = self.dic_information_db_engines[db_engine_type]

            if table_name in dic_table_columns:
                ar_fields = dic_table_columns[table_name]

        return ar_fields
