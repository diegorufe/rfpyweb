"""

    This module is base for DAOS

"""
from transactions.enum_db_engine_type import EnumDbEngineType
from utils.str.rf_utils_str import RFUtilsStr
from context.rf_context import RFContext
from beans.query.field import Field
from utils.db.rf_utils_db import RFUtilsDb


class RFBaseDao:

    def __init__(self, vo_class=None, db_engine_type: EnumDbEngineType = EnumDbEngineType.RF_MYSQL):
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
        pass

    def edit(self, vo, params=None, rf_transaction=None, locale=None):
        pass

    def read(self, id, ar_joins=None, params=None, rf_transaction=None, locale=None):
        pass

    def delete(self, id, params=None, rf_transaction=None, locale=None):
        pass

    def list(self, ar_fields=None, ar_filters=None, ar_joins=None, ar_orders=None, ar_groups=None, limits=None,
             params=None, rf_transaction=None, locale=None):

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

        # Build orderby

        # Build limit

        query_builder = query_builder_select + query_builder_form + query_builder_joins + query_builder_where

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
