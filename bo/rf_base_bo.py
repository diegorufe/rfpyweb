""""
    Base module for bo
"""
from transactions.transaction_decorator import transaction_decorator
from transactions.enum_transaction_type import EnumTransactionType


class RFBaseBo:

    def __init__(self, dao=None):
        """
        Constructor for base bo
        :param dao: dao for bo. Can be None
        """
        self.dao = dao

    @transaction_decorator(EnumTransactionType.PROPAGATED)
    def add(self, vo, params=None, rf_transaction=None, locale=None):
        """
        Method for add vo
        :param vo:
        :param params:
        :param rf_transaction:
        :param locale:
        :return: vo inserted
        """
        return self.dao.add(vo=vo, params=params, rf_transaction=rf_transaction, locale=locale)

    @transaction_decorator(EnumTransactionType.PROPAGATED)
    def edit(self, vo, params=None, rf_transaction=None, locale=None, ):
        """
        Method for edit vo
        :param vo: to edit
        :param params:
        :param rf_transaction:
        :param locale:
        :return: vo edited
        """
        return self.dao.edit(vo=vo, params=params, rf_transaction=rf_transaction, locale=locale)

    @transaction_decorator(EnumTransactionType.PROPAGATED)
    def delete(self, ar_pks_values, params=None, rf_transaction=None, locale=None):
        """
        Method for delete vo by pks values
        :param ar_pks_values:
        :param params:
        :param rf_transaction:
        :param locale:
        :return: number of records delete
        """
        return self.dao.delete(ar_pks_values=ar_pks_values, params=params,
                               rf_transaction=rf_transaction, locale=locale)

    @transaction_decorator(EnumTransactionType.PROPAGATED)
    def read(self, ar_pks_values, ar_joins=None, params=None, rf_transaction=None, locale=None):
        return self.dao.read(ar_pks_values=ar_pks_values, ar_joins=ar_joins, params=params,
                             rf_transaction=rf_transaction, locale=locale)

    @transaction_decorator(EnumTransactionType.PROPAGATED)
    def count(self, ar_filters=None, ar_joins=None,
              params=None, rf_transaction=None, locale=None):
        """
        Method for count query
        :param ar_filters:
        :param ar_joins:
        :param params:
        :param rf_transaction:
        :param locale:
        :return: number of registers
        """
        return self.dao.count(ar_filters=ar_filters, ar_joins=ar_joins, params=params, rf_transaction=rf_transaction,
                              locale=locale)

    @transaction_decorator(EnumTransactionType.PROPAGATED)
    def list(self, ar_fields=None, ar_filters=None, ar_joins=None, ar_orders=None, ar_groups=None, limit=None,
             params=None, rf_transaction=None, locale=None, ):
        """
        Method for list query
        :param ar_fields:
        :param ar_filters:
        :param ar_joins:
        :param ar_orders:
        :param ar_groups:
        :param limit:
        :param params:
        :param rf_transaction:
        :param locale:
        :return: list data for query
        """
        return self.dao.list(ar_fields=ar_fields, ar_filters=ar_filters, ar_joins=ar_joins,
                             ar_orders=ar_orders,
                             ar_groups=ar_groups,
                             limit=limit,
                             params=params, rf_transaction=rf_transaction, locale=locale)

    @transaction_decorator(EnumTransactionType.REQUIRED_NEVER)
    def new_instance_vo(self, rf_transaction=None):
        """
        Method for build new instance vo
        :param rf_transaction:
        :return: instance vo
        """
        return self.dao.new_instance_vo(rf_transaction=rf_transaction)

    def vo_class(self):
        """
        Method for get vo class
        :return: vo class
        """
        return self.dao.vo_class

    def vo_class_name(self):
        """
        Method for get vo class name
        :return: vo class name
        """
        return self.vo_class().__name__
