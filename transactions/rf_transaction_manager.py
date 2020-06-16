"""

 Class for manage transactions

"""
from transactions.enum_transaction_type import EnumTransactionType
from transactions.enum_db_engine_type import EnumDbEngineType
from context.rf_context import RFContext
from transactions.rf_transaction import RFTransaction


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

    def create_transaction(self, enum_transaction_type: EnumTransactionType = EnumTransactionType.PROPAGATED,
                           params=None, db_engine_type: EnumDbEngineType = EnumDbEngineType.RF_MYSQL):
        """
        Method for create transaction
        :param enum_transaction_type:  type for transaction to create
        :param params
        :param db_engine_type engine for db
        :return: response for transaction create
        """
        # set default transaction propagated
        enum_transaction_type = enum_transaction_type if not None else EnumTransactionType.PROPAGATED
        response = None
        if self.function_create_transaction is not None:
            response = self.function_create_transaction(enum_transaction_type, params=params,
                                                        db_engine_type=db_engine_type)
        else:
            if db_engine_type == EnumDbEngineType.RF_MYSQL:
                rf_mysql_engine = RFContext.get_db_engine(EnumDbEngineType.RF_MYSQL)
                if rf_mysql_engine is not None:
                    response = RFTransaction(enum_transaction_type, transaction_database=rf_mysql_engine.connect())

        return response

    def commit(self, rf_transaction: RFTransaction, params=None):
        """
        Method for commit transaction
        :param rf_transaction:
        :param params
        :return: response for commit transaction
        """
        response = False
        try:
            if rf_transaction is not None and self.function_commit_transaction is not None:
                response = self.function_commit_transaction(rf_transaction, params)
            elif rf_transaction is not None:
                if rf_transaction.db_engine_type == EnumDbEngineType.RF_MYSQL:
                    rf_transaction.transaction_database.commit()
                    rf_transaction.transaction_database.close()
                    response = True
        except Exception as ex:
            response = False
        # If response is False rollback transaction
        if response is False:
            self.rollback(rf_transaction, params=params)
        return response

    def rollback(self, rf_transaction: RFTransaction, params=None):
        """
        Method for rollback transaction
        :param rf_transaction:  to rollback
        :param params
        :return: response for rollback transaction
        """
        response = False
        if rf_transaction is not None and self.function_rollback_transaction is not None:
            response = self.function_commit_transaction(rf_transaction, params=params)
        elif rf_transaction is not None:
            if rf_transaction.db_engine_type == EnumDbEngineType.RF_MYSQL:
                rf_transaction.transaction_database.rollback()
                rf_transaction.transaction_database.close()
                response = True

        return response
