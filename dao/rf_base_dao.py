"""

    This module is base for DAOS

"""
from transactions.enum_db_engine_type import EnumDbEngineType
from utils.str.rf_utils_str import RFUtilsStr
from utils.array.rf_utils_array import RFUtilsArray
from constants.enum_join_type import EnumJoinType
from constants.constants_associations import JOIN_ASSOCIATION_SEPARATOR


class RFBaseDao:

    def __init__(self, vo_class=None, db_engine_type: EnumDbEngineType = EnumDbEngineType.RF_MYSQL):
        """
        Constructor for dao
        :param vo_class is a class vo data
        :param db_engine_type: default value is EnumDbEngineType.RF_MYSQL
        """
        RFBaseDao.__init__(self)
        self.vo_class = vo_class
        self.db_engine_type = db_engine_type
        self._table_name = self.vo_class().table_name
        self._fields_table = None

    def get_table_name(self):
        """
        Method for get table table for dao
        :return: name for table for dao
        """
        return self._table_name

    def add(self, locale, vo, params=None, rf_transaction=None):
        pass

    def edit(self, locale, vo, params=None, rf_transaction=None):
        pass

    def read(self, locale, id, ar_joins=None, params=None, rf_transaction=None):
        pass

    def delete(self, locale, id, params=None, rf_transaction=None):
        pass

    def list(self, locale, ar_fields=None, ar_filters=None, ar_joins=None, ar_orders=None, ar_groups=None, limits=None,
             params=None, rf_transaction=None):

        # Query builder
        query_builder = ""

        # Build select
        query_builder_select = self.__build_select_query__(
            ar_fields_query=self.__get_fields_query__(ar_fields, rf_transaction), ar_joins_query=ar_joins)

        # Build from
        query_builder_form = self.__build_from_query__()

        # Build joins
        query_builder_joins = self.__build_joins_query__(ar_joins)

        # Build where
        # TODO

    def __get_fields_query__(self, ar_fields, rf_transaction):
        """
        Method for get fields to get in query
        :param ar_fields: passed for list function
        :param rf_transaction: to execute query
        :return: ar fields to get in query
        """
        find_all_fields = RFUtilsArray.is_empty(ar_fields)
        ar_fields_query = []

        if self.db_engine_type == EnumDbEngineType.RF_MYSQL:
            # Find all field raw columns for table
            if find_all_fields and rf_transaction is not None:
                ar_fields_query = self._fields_table
            else:
                ar_fields_query = ar_fields

        return ar_fields_query

    def __build_select_query__(self, ar_fields_query=None, ar_joins_query=None):
        """
        Method for build select query
        :param ar_fields_query: to get in query
        :param ar_joins_query: joins for query. Is necessary if has join is fetch
        :return: select query
        """
        query_builder = ""

        # Engine EnumDbEngineType.RF_MYSQL
        if self.db_engine_type == EnumDbEngineType.RF_MYSQL:
            query_builder = " SELECT "

            if RFUtilsArray.is_not_empty(ar_fields_query):
                first = True
                for field in ar_fields_query:
                    if not first:
                        query_builder = query_builder + " , "

                    if RFUtilsStr.is_not_emtpy(field.alias_table):
                        query_builder = query_builder + " " + field.alias_table.strip() + "."
                    else:
                        query_builder = query_builder + " " + self._table_name.strip() + "."

                    query_builder = query_builder + field.name.strip()

                    query_builder = query_builder

                    if RFUtilsStr.is_not_emtpy(field.alias_field):
                        query_builder = query_builder + " " + field.alias_field.strip() + " "
                    else:
                        query_builder = query_builder + " " + field.name.strip() + " "

                    first = False
            else:
                query_builder = query_builder + " " + self._table_name + ".* "

            # Check joins for get data
            if RFUtilsArray.is_not_empty(ar_joins_query):
                # For each join add if join fetch
                ar_joins_fetch = [EnumJoinType.INNER_JOIN_FETCH, EnumJoinType.LEFT_JOIN_FETCH,
                                  EnumJoinType.RIGHT_JOIN_FETCH]
                for join in ar_joins_query:
                    # Add join if fetch for join table. Only join for non alias table by the moment
                    if join.join_type is not None and join.join_type in ar_joins_fetch and RFUtilsStr.is_not_emtpy(
                            join.join_table) and RFUtilsStr.is_not_emtpy(join.join_field) and \
                            RFUtilsStr.is_empty(join.join_alias):
                        # TODO join fetch with alias. Check if this is correct
                        query_builder = query_builder + ", " + self._table_name + \
                                        JOIN_ASSOCIATION_SEPARATOR + join.join_field + ".* "

        return query_builder

    def __build_from_query__(self):
        """
        Method for build from query
        :return: from query
        """
        query_builder = ""

        # Engine EnumDbEngineType.RF_MYSQL
        if self.db_engine_type == EnumDbEngineType.RF_MYSQL:
            query_builder = " FROM " + self._table_name + " as " + self._table_name

        return query_builder

    def __build_joins_query__(self, ar_joins_query):
        """
        Method for build joins query
        :param ar_joins_query: to build
        :return: joins for query
        """
        query_builder = ""

        if RFUtilsArray.is_not_empty(ar_joins_query):
            for join in ar_joins_query:
                if self.db_engine_type == EnumDbEngineType.RF_MYSQL:
                    # TODO
                    pass

        return query_builder
