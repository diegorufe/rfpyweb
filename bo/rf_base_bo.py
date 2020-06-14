""""
    Base module for bo
"""
from transactions.transaction_decorator import transaction_decorator
from transactions.enum_transaction_type import EnumTransactionType
from transactions.rf_transaction_manager import RFTransactionManager


class RFBaseBo:

    def __init__(self, dao=None, transaction_manager: RFTransactionManager = None):
        """
        Constructor for base bo
        :param dao: dao for bo,. Can be None
        :param transaction_manager: for manage transactions. Can be None
        """
        self.dao = dao

        # Set fields for table in dalo
        if self.dao is not None:
            self.dao._fields_table = transaction_manager.get_fields_table(self.dao.get_table_name(),
                                                                          self.dao.db_engine_type)
        self.transaction_manager = transaction_manager

    @transaction_decorator(EnumTransactionType.PROPAGATED)
    def add(self, locale, vo, params=None, rf_transaction=None):
        pass

    @transaction_decorator(EnumTransactionType.PROPAGATED)
    def edit(self, locale, vo, params=None, rf_transaction=None):
        pass

    @transaction_decorator(EnumTransactionType.PROPAGATED)
    def delete(self, locale, id, params=None, rf_transaction=None):
        pass

    @transaction_decorator(EnumTransactionType.PROPAGATED)
    def read(self, locale, id, ar_joins=None, params=None, rf_transaction=None):
        pass

    @transaction_decorator(EnumTransactionType.PROPAGATED)
    def list(self, locale, ar_fields=None, ar_filters=None, ar_joins=None, ar_orders=None, ar_groups=None, limits=None,
             params=None, rf_transaction=None):
        return self.dao.list(locale, ar_fields=None, ar_filters=None, ar_joins=None, ar_orders=None, ar_groups=None,
                             limits=None,
                             params=None, rf_transaction=None)
