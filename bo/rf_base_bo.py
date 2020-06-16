""""
    Base module for bo
"""
from transactions.transaction_decorator import transaction_decorator
from transactions.enum_transaction_type import EnumTransactionType
from transactions.rf_transaction_manager import RFTransactionManager


class RFBaseBo:

    def __init__(self, dao=None):
        """
        Constructor for base bo
        :param dao: dao for bo,. Can be None
        """
        self.dao = dao

    @transaction_decorator(EnumTransactionType.PROPAGATED)
    def add(self, vo, params=None, rf_transaction=None, locale=None):
        pass

    @transaction_decorator(EnumTransactionType.PROPAGATED)
    def edit(self, vo, params=None, rf_transaction=None, locale=None, ):
        pass

    @transaction_decorator(EnumTransactionType.PROPAGATED)
    def delete(self, id, params=None, rf_transaction=None, locale=None, ):
        pass

    @transaction_decorator(EnumTransactionType.PROPAGATED)
    def read(self, id, ar_joins=None, params=None, rf_transaction=None, locale=None, ):
        pass

    @transaction_decorator(EnumTransactionType.PROPAGATED)
    def list(self, ar_fields=None, ar_filters=None, ar_joins=None, ar_orders=None, ar_groups=None, limits=None,
             params=None, rf_transaction=None, locale=None, ):
        return self.dao.list(ar_fields=ar_fields, ar_filters=ar_filters, ar_joins=ar_joins,
                             ar_orders=ar_orders,
                             ar_groups=ar_groups,
                             limits=limits,
                             params=params, rf_transaction=rf_transaction, locale=locale)
