"""
    Module for manage transactions for daos
"""
from transactions.enum_transaction_type import EnumTransactionType


class RFTransaction:

    def __init__(self, enum_transaction_type: EnumTransactionType, transaction_database=None):
        """
        Constructor for class transactions database
        :param enum_transaction_type:  type for transaction
        :param transaction_database:  is transaction database to apply
        """
        self.enum_transaction_type = enum_transaction_type if not None else EnumTransactionType.PROPAGATED
        self.transaction_database = transaction_database
