"""

    Module decorator transactions

"""
from transactions.enum_transaction_type import EnumTransactionType


def transaction_decorator(enum_transaction_type: EnumTransactionType):
    def decorator_func(f):
        def wrapper_func(self, *args, **kwargs):
            # Invoke the wrapped function first
            print("Transaction type: " + str(enum_transaction_type))
            response = f(*args, **kwargs)
            return response

        return wrapper_func

    return decorator_func
