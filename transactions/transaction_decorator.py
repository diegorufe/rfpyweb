"""

    Module decorator transactions

"""
from transactions.enum_transaction_type import EnumTransactionType
from core.constants.rf_core_constants import APP_ENABLE_LOG_TRANSACTION_DECORATOR
from context.rf_context import RFContext
import time
from log.rf_logger import RFLogger


def transaction_decorator(enum_transaction_type: EnumTransactionType):
    def decorator_func(f):
        def wrapper_func(self, *args, **kwargs):

            rf_transaction = None
            transaction_propagated_created = False

            try:
                time_ns = time.time_ns()

                if APP_ENABLE_LOG_TRANSACTION_DECORATOR:
                    RFLogger.debug("Transaction type: " + str(enum_transaction_type))

                #  EnumTransactionType.PROPAGATED
                if enum_transaction_type == EnumTransactionType.PROPAGATED:

                    if 'rf_transaction' not in kwargs:
                        rf_transaction = RFContext.get_transaction_manager().create_transaction(
                            enum_transaction_type=EnumTransactionType.PROPAGATED_CREATED)
                        kwargs['rf_transaction'] = rf_transaction
                        transaction_propagated_created = True
                    else:
                        rf_transaction = kwargs['rf_transaction']

                # EnumTransactionType.REQUIRED_NEW
                elif enum_transaction_type == EnumTransactionType.REQUIRED_NEW:
                    rf_transaction = RFContext.get_transaction_manager().create_transaction(
                        enum_transaction_type=enum_transaction_type)
                    kwargs['rf_transaction'] = rf_transaction

                # EnumTransactionType.REQUIRED_NEVER
                elif enum_transaction_type == EnumTransactionType.REQUIRED_NEVER and 'rf_transaction' not in kwargs:
                    kwargs['rf_transaction'] = None

                # Execute method
                response = f(self, *args, **kwargs)

                # commit transaction if necessary
                if transaction_propagated_created is True or enum_transaction_type == EnumTransactionType.REQUIRED_NEW:
                    RFContext.get_transaction_manager().commit(rf_transaction)

                if APP_ENABLE_LOG_TRANSACTION_DECORATOR:
                    time_ns = time.time_ns() - time_ns
                    RFLogger.debug("Time execute transaction in in function " + str(f.__name__) + ", for class " + str(
                        self) + ", ns: "+ str(time_ns))

                return response
            except Exception as ex:

                # If transaction is not none execute rollback
                if rf_transaction is not None:
                    RFContext.get_transaction_manager().rollback(rf_transaction)

                if APP_ENABLE_LOG_TRANSACTION_DECORATOR:
                    RFLogger.debug("Error in function  " + str(f.__name__) + ", for class " + str(self))
                    RFLogger.debug("Error in Transaction type: " + str(enum_transaction_type))
                    RFLogger.debug("Error transaction decorator " + str(ex))

                raise ex

        return wrapper_func

    return decorator_func
