"""

    This module is base for DAOS

"""
from transactions.enum_db_engine_type import EnumDbEngineType
from utils.str.rf_utils_str import RFUtilsStr
from utils.array.rf_utils_array import RFUtilsArray
from constants.enum_join_type import EnumJoinType
from constants.constants_associations import JOIN_ASSOCIATION_SEPARATOR, FIELD_TABLE_SEPARATOR
from context.rf_context import RFContext
from utils.built.rf_utils_built import RFUtilsBuilt


class RFBaseDao:

    def __init__(self, vo_class=None, db_engine_type: EnumDbEngineType = EnumDbEngineType.RF_MYSQL):
        """
        Constructor for dao
        :param vo_class is a class vo data
        :param db_engine_type: default value is EnumDbEngineType.RF_MYSQL
        """
        self.vo_class = vo_class
        self.db_engine_type = db_engine_type
        self._table_name = self.vo_class().table_name
        self._fields_table = None

        # Load fields for db engine
        if RFUtilsStr.is_not_emtpy(self._table_name) and self.db_engine_type is not None:
            self._fields_table = RFContext.get_fields_table(self._table_name, db_engine_type)

    def get_table_name(self):
        """
        Method for get table table for dao
        :return: name for table for dao
        """
        return self._table_name

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

        dic_params = {}

        # Build select
        query_builder_select = self.__build_select_query__(
            ar_fields_query=self.__get_fields_query__(ar_fields, rf_transaction), ar_joins_query=ar_joins)

        # Build from
        query_builder_form = self.__build_from_query__()

        # Build joins
        query_builder_joins = self.__build_joins_query__(ar_joins)

        # Build where
        # TODO

        # Build groupby

        # Build orderby

        # Build limit

        query_builder = query_builder_select + query_builder_form + query_builder_joins

        ar_data = rf_transaction.execute_list_query(query_builder, dic_params=dic_params)

        ar_response = []

        if ar_data is not None:
            vo_instance = None
            old_instance = None
            for data in ar_data:

                vo_instance = self.vo_class()
                for key in data:
                    old_instance = vo_instance
                    ar_key_split = RFUtilsStr.split(key, FIELD_TABLE_SEPARATOR)

                    if RFUtilsArray.is_not_empty(ar_key_split):
                        ar_key_split.pop(0)

                        for field in ar_key_split:
                            if RFUtilsBuilt.has_attr(old_instance, field):
                                RFUtilsBuilt.set_attr(old_instance, field, data[key])
                                old_instance = RFUtilsBuilt.get_attr(old_instance, field)

                ar_response.append(vo_instance)

        return ar_response

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

            # Load selected fields
            if RFUtilsArray.is_not_empty(ar_fields_query):
                first = True
                for field in ar_fields_query:
                    if not first:
                        query_builder = query_builder + " , "

                    if RFUtilsStr.is_not_emtpy(field.alias_table):
                        query_builder = query_builder + " " + field.alias_table.strip() + "."
                    else:
                        query_builder = query_builder + " " + self.get_table_name().strip() + "."

                    query_builder = query_builder + field.name.strip()

                    if RFUtilsStr.is_not_emtpy(field.alias_field):
                        query_builder = query_builder + " " + field.alias_field.strip() + " "
                    else:
                        query_builder = query_builder + " " + \
                                        self.get_table_name() + FIELD_TABLE_SEPARATOR + field.name.strip() + " "

                    first = False

            # Load all fields
            elif RFUtilsArray.is_not_empty(self._fields_table):
                first = True
                for field in self._fields_table:
                    if not first:
                        query_builder = query_builder + " , "
                    query_builder = query_builder + " " + \
                                    self._table_name + "." + field.name.strip() + " " + \
                                    self._table_name + FIELD_TABLE_SEPARATOR + field.name.strip() + " "

                    first = False

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
                        ar_fields_join = RFContext.get_fields_table(join.join_table)
                        if RFUtilsArray.is_not_empty(ar_fields_join):
                            for field in ar_fields_join:
                                query_builder = query_builder + ", " + self._table_name + \
                                                JOIN_ASSOCIATION_SEPARATOR + join.join_table + "." + field.name \
                                                + "  " + self._table_name \
                                                + JOIN_ASSOCIATION_SEPARATOR + join.join_field \
                                                + FIELD_TABLE_SEPARATOR + field.name

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

                    if RFUtilsStr.is_not_emtpy(join.custom_query_join):
                        query_builder = query_builder + " " + join.custom_query_join
                    else:
                        join_type = " INNER JOIN "

                        if join.join_type == EnumJoinType.RIGHT_JOIN or \
                                join.join_type == EnumJoinType.RIGHT_JOIN_FETCH:
                            join_type = " INNER JOIN "
                        elif join.join_type == EnumJoinType.LEFT_JOIN or \
                                join.join_type == EnumJoinType.LEFT_JOIN_FETCH:
                            join_type = " LEFT JOIN "
                        elif join.join_type == EnumJoinType.RIGHT_JOIN or \
                                join.join_type == EnumJoinType.RIGHT_JOIN_FETCH:
                            join_type = " RIGHT JOIN "

                        query_builder = query_builder + " " + join_type + " " + join.join_table

                        if RFUtilsStr.is_not_emtpy(join.join_alias):
                            query_builder = query_builder + " AS " + join.join_alias
                            query_builder = query_builder + " ON " + join.join_alias + "." + join.join_table_field \
                                            + " = " + self._table_name + join.join_field
                        else:
                            query_builder = query_builder + " AS " + self._table_name + JOIN_ASSOCIATION_SEPARATOR + \
                                            join.join_field + " "
                            query_builder = query_builder + " ON " + self._table_name + JOIN_ASSOCIATION_SEPARATOR + \
                                            join.join_field + "." + join.join_table_field \
                                            + " = " + self._table_name + join.join_table_field

        return query_builder
