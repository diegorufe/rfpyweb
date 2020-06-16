"""

    Module decorator transactions

"""
from transactions.enum_transaction_type import EnumTransactionType
from constants.constants_log import ENABLE_LOG_TRANSACTION_DECORATOR


def transaction_decorator(enum_transaction_type: EnumTransactionType):
    def decorator_func(f):
        def wrapper_func(self, *args, **kwargs):
            response = None
            try:
                if ENABLE_LOG_TRANSACTION_DECORATOR:
                    print("Transaction type: " + str(enum_transaction_type))

                response = f(*args, **kwargs)

                return response
            except Exception as ex:
                if ENABLE_LOG_TRANSACTION_DECORATOR:
                    print("Error in Transaction type: " + str(enum_transaction_type))
                    print("Error transaction decorator " + str(ex))

        return wrapper_func

    return decorator_func
