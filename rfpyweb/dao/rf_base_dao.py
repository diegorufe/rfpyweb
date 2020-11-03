"""

    This module is base for DAOS

"""
from rfpyweb.transactions.enum_db_engine_type import EnumDbEngineType
from rfpyutils.str.rf_utils_str import RFUtilsStr, DOT
from rfpyweb.context.rf_context import RFContext
from rfpyweb.beans.query.field import Field
from rfpyweb.beans.query.filter import Filter
from rfpyweb.beans.query.limit import Limit
from rfpyweb.utils.db.rf_utils_db import RFUtilsDb
from rfpyutils.built.rf_utils_built import RFUtilsBuilt
from rfpyutils.array.rf_utils_array import RFUtilsArray
import datetime
from rfpyweb.constants.constants_associations import DEFAULT_ALIAS


class RFBaseDao:

    def __init__(self, vo_class=None, db_engine_type: EnumDbEngineType = EnumDbEngineType.RF_MYSQL_POOL):
        """
        Constructor for dao
        :param vo_class is a class vo data
        :param db_engine_type: default value is EnumDbEngineType.RF_MYSQL
        """
        self.vo_class = vo_class
        self.db_engine_type = db_engine_type
        self._table_name = self.vo_class.__table_name__
        self._columns_table = None
        self._fields_table = []
        self._vo_class_name = self.vo_class.__name__

        # Load fields for db engine
        if RFUtilsStr.is_not_emtpy(self._vo_class_name) and self.db_engine_type is not None:
            self._columns_table = RFContext.get_columns_table(self._vo_class_name)

            if self._columns_table is not None:
                for key_column in self._columns_table:
                    column = self._columns_table[key_column]
                    self._fields_table.append(Field(column.name))

    def get_table_name(self):
        """
        Method for get table table for dao
        :return: name for table for dao
        """
        return self._table_name

    def get_vo_class_name(self):
        """
        Method for get vo class name
        :return: vo class name
        """
        return self._vo_class_name

    def add(self, vo, params=None, rf_transaction=None, locale=None):
        """
        Method for add in query
        :param vo: to add
        :param params:
        :param rf_transaction:
        :param locale:
        :return: vo inserted
        """
        # Audit create vo
        if RFUtilsBuilt.has_attr(vo, "createdAt"):
            RFUtilsBuilt.set_attr(vo, "createdAt", datetime.datetime.now())

        # Audit update vo
        if RFUtilsBuilt.has_attr(vo, "updatedAt"):
            RFUtilsBuilt.set_attr(vo, "updatedAt", datetime.datetime.now())

        dic_params_query = {}
        query_builder_insert = RFUtilsDb.build_insert_query(vo_instance=vo, dic_params_query=dic_params_query)
        result = rf_transaction.execute_query(query_builder_insert, dic_params_query=dic_params_query, insert=True)

        # set latest pk inserted
        if len(vo.__ar_pk_fields__) == 1:
            RFUtilsBuilt.set_attr(vo, vo.__ar_pk_fields__[0], result)

        return vo

    def edit(self, vo, params=None, rf_transaction=None, locale=None):
        """
        Method for edit vo
        :param vo: to edit
        :param params:
        :param rf_transaction:
        :param locale:
        :return: vo edited
        """
        # Audit update vo
        if RFUtilsBuilt.has_attr(vo, "updatedAt"):
            RFUtilsBuilt.set_attr(vo, "updatedAt", datetime.datetime.now())

        dic_params_query = {}
        query_builder_update = RFUtilsDb.build_update_query(vo_instance=vo, dic_params_query=dic_params_query)
        rf_transaction.execute_query(query_builder_update, dic_params_query=dic_params_query)
        return vo

    def read(self, ar_pks_values, ar_joins=None, params=None, rf_transaction=None, locale=None):
        """
        Method for read vo
        :param ar_pks_values: for vo
        :param ar_joins:
        :param params:
        :param rf_transaction:
        :param locale:
        :return:
        """
        ar_filters = self.__get_pk_filters__(ar_pks_values)
        limit = Limit(0, 1)
        result_list = self.list(ar_filters=ar_filters, ar_joins=ar_joins, limit=limit, rf_transaction=rf_transaction)

        result = result_list[0] if RFUtilsArray.is_not_empty(result_list) else None

        return result

    def delete(self, ar_pks_values, params=None, rf_transaction=None, locale=None):
        """
        Method for delete vo for pk values
        :param ar_pks_values:
        :param params:
        :param rf_transaction:
        :param locale:
        :return: number of records delete
        """
        dic_params_query = {}
        ar_filters = self.__get_pk_filters__(ar_pks_values)

        query_builder_delete = "DELETE " + DEFAULT_ALIAS + " "

        # Build from
        query_builder_form = self.__build_from_query__()

        # Build where
        query_builder_where = self.__build_where_query__(ar_filters_query=ar_filters, dic_params_query=dic_params_query)

        query_builder = query_builder_delete + query_builder_form + query_builder_where

        result = rf_transaction.execute_query(query_builder, dic_params_query=dic_params_query)

        return result

    def count(self, ar_filters=None, ar_joins=None,
              params=None, rf_transaction=None, locale=None):
        """
        Method for count data for database
        :param ar_filters:
        :param ar_joins:
        :param params:
        :param rf_transaction:
        :param locale:
        :return: count registers
        """
        dic_params_query = {}

        # Build select
        query_builder_select = "SELECT COUNT(*) "

        # Build from
        query_builder_form = self.__build_from_query__()

        # Build joins
        query_builder_joins = self.__build_joins_query__(ar_joins)

        # Build where
        query_builder_where = self.__build_where_query__(ar_filters_query=ar_filters, dic_params_query=dic_params_query)

        query_builder = query_builder_select + query_builder_form + query_builder_joins + query_builder_where

        result = rf_transaction.execute_query(query_builder, dic_params_query=dic_params_query, count=True)

        return result

    def list(self, ar_fields=None, ar_filters=None, ar_joins=None, ar_orders=None, ar_groups=None, limit=None,
             params=None, rf_transaction=None, locale=None):
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
        :return: list of query
        """
        dic_params_query = {}

        # Build select
        query_builder_select = self.__build_select_query__(
            ar_fields_query=self.__get_fields_query__(ar_fields, rf_transaction), ar_joins_query=ar_joins)

        # Build from
        query_builder_form = self.__build_from_query__()

        # Build joins
        query_builder_joins = self.__build_joins_query__(ar_joins)

        # Build where
        query_builder_where = self.__build_where_query__(ar_filters_query=ar_filters, dic_params_query=dic_params_query)

        # Build groupby
        # TODO
        # Build orderby
        query_builder_order = self.__build_order_query__(ar_orders=ar_orders)

        # Build limit
        query_builder_limit = self.__build_limit_query__(limit=limit, dic_params_query=dic_params_query)

        query_builder = query_builder_select + query_builder_form + query_builder_joins + query_builder_where + \
                        query_builder_order + query_builder_limit

        ar_data = rf_transaction.execute_list_query(query_builder, dic_params_query=dic_params_query)

        ar_response = RFUtilsDb.fetch_value_query(self.vo_class, ar_data)

        return ar_response

    def __get_fields_query__(self, ar_fields, rf_transaction):
        """
        Method for get fields to get in query
        :param ar_fields: passed for list function
        :param rf_transaction: to execute query
        :return: ar fields to get in query
        """
        return RFUtilsDb.get_fields_query(ar_fields=ar_fields, rf_transaction=rf_transaction,
                                          db_engine_type=self.db_engine_type,
                                          ar_default_fields_table=self._fields_table)

    def __build_select_query__(self, ar_fields_query=None, ar_joins_query=None):
        """
        Method for build select query
        :param ar_fields_query: to get in query
        :param ar_joins_query: joins for query. Is necessary if has join is fetch
        :return: select query
        """
        return RFUtilsDb.build_select_query(ar_fields_query=ar_fields_query, ar_joins_query=ar_joins_query,
                                            db_engine_type=self.db_engine_type,
                                            ar_default_fields_table=self._fields_table,
                                            vo_class_name=self._vo_class_name)

    def __build_from_query__(self):
        """
        Method for build from query
        :return: from query
        """
        return RFUtilsDb.build_from_query(db_engine_type=self.db_engine_type, table_name=self._table_name)

    def __build_joins_query__(self, ar_joins_query):
        """
        Method for build joins query
        :param ar_joins_query: to build
        :return: joins for query
        """
        return RFUtilsDb.build_joins_query(db_engine_type=self.db_engine_type, ar_joins_query=ar_joins_query,
                                           vo_class_name=self._vo_class_name)

    def __build_where_query__(self, ar_filters_query=None, dic_params_query={}):
        """
        Mhetod for build where query
        :param ar_filters_query: to apply
        :param dic_params_query: for add to apply in engine database
        :return: builder with query built with filters to apply
        """
        return RFUtilsDb.build_where_query(ar_filters_query=ar_filters_query, dic_params_query=dic_params_query,
                                           db_engine_type=self.db_engine_type)

    def __build_order_query__(self, ar_orders=None):
        """
        Method for build order query
        :param ar_orders:  orders for build
        :return: order query
        """
        return RFUtilsDb.build_order_query(ar_orders=ar_orders, db_engine_type=self.db_engine_type)

    def __build_limit_query__(self, limit=None, dic_params_query={}):
        """
        Method for muild limit
        :param limit: to build
        :param dic_params_query: to set limit query
        :return: build limit query
        """
        return RFUtilsDb.build_limit(limit=limit, dic_params_query=dic_params_query)

    def new_instance_vo(self, rf_transaction=None):
        """
        Method for build new instance vo
        :param rf_transaction:
        :return: instance vo
        """
        return self.vo_class()

    def __get_pk_filters__(self, ar_pks_values):
        """
        Method for get pk filters
        :param ar_pks_values: to set in filters
        :return: array pk filters
        """
        ar_filters = []
        for index, pk in enumerate(self.vo_class.__ar_pk_fields__):
            rf_column = RFContext.get_column_table(self.vo_class.__name__, pk)

            if RFUtilsStr.is_not_emtpy(rf_column.join_table):
                ar_filters.append(Filter(field=pk + DOT + rf_column.column_name, value=ar_pks_values[index]))
            else:
                ar_filters.append(Filter(field=pk, value=ar_pks_values[index]))
        return ar_filters
