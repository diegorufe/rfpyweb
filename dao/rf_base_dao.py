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
from constants.enum_filter_type import EnumFilterType
from constants.enum_filter_operation_type import EnumFilterOperationType


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
                        query_builder = query_builder + " " + self._table_name.strip() + "."

                    query_builder = query_builder + field.name.strip()

                    if RFUtilsStr.is_not_emtpy(field.alias_field):
                        query_builder = query_builder + " " + field.alias_field.strip() + " "
                    else:
                        query_builder = query_builder + " " + \
                                        self._table_name + FIELD_TABLE_SEPARATOR + field.name.strip() + " "

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
                        ar_fields_join = RFContext.get_fields_table(join.join_table, self.db_engine_type)
                        if RFUtilsArray.is_not_empty(ar_fields_join):
                            for field in ar_fields_join:
                                query_builder = query_builder + ", " + self._table_name + \
                                                JOIN_ASSOCIATION_SEPARATOR + join.join_field + "." + field.name \
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
                                            + " = " + self._table_name + "." + join.join_field
                        else:
                            query_builder = query_builder + " AS " + self._table_name + JOIN_ASSOCIATION_SEPARATOR + \
                                            join.join_field + " "
                            query_builder = query_builder + " ON " + self._table_name + JOIN_ASSOCIATION_SEPARATOR + \
                                            join.join_field + "." + join.join_table_field \
                                            + " = " + self._table_name + "." + join.join_table_field

        return query_builder

    def __build_where_query__(self, ar_filters_query=None, dic_params_query={}):
        """
        Mhetod for build where query
        :param ar_filters_query: to apply
        :param dic_params_query: for add to apply in engine database
        :return: builder with query built with filters to apply
        """
        query_builder = ""
        query_builder_partial = ""
        open_brackets = 1
        closed_brackets = 1
        query_builder_where = ""

        if RFUtilsArray.is_not_empty(ar_filters_query):

            first: bool = True

            for filter_query in ar_filters_query:

                query_builder_partial = ""

                if self.db_engine_type == EnumDbEngineType.RF_MYSQL:
                    filter_type = filter_query.filter_type

                    if filter_type is not None:

                        query_builder_where = " WHERE "

                        open_brackets = filter_query.open_brackets if filter_query.open_brackets is not None and \
                                                                      filter_query.open_brackets > 0 else 1
                        closed_brackets = filter_query.closed_brackets if filter_query.closed_brackets is not None and \
                                                                          filter_query.closed_brackets > 0 else 1

                        if first is False:
                            query_builder_partial = query_builder_partial + " " + \
                                                    " AND " if filter_query.filter_operation_type == \
                                                               EnumFilterOperationType.AND else " OR "

                        # open brackets
                        counter = 0
                        while counter < open_brackets:
                            counter = counter + 1
                            query_builder_partial = query_builder_partial + " ( "

                        alias = filter_query.alias if RFUtilsStr.is_not_emtpy(filter_query.alias) else self._table_name
                        key_param = RFUtilsStr.unique_str()

                        # " = "
                        if filter_type == EnumFilterType.EQUAL:
                            dic_params_query[key_param] = filter_query.value
                            query_builder_partial = query_builder_partial + " " + alias + "." + filter_query.field + \
                                                    " =  %(" + key_param + ")s "

                        # " != "
                        elif filter_type == EnumFilterType.DISTINCT:
                            dic_params_query[key_param] = filter_query.value
                            query_builder_partial = query_builder_partial + " " + alias + "." + filter_query.field + \
                                                    " != %(" + key_param + ")s "

                        # " >= "
                        elif filter_type == EnumFilterType.GE:
                            dic_params_query[key_param] = filter_query.value
                            query_builder_partial = query_builder_partial + " " + alias + "." + filter_query.field + \
                                                    " >= %(" + key_param + ")s "

                        # " > "
                        elif filter_type == EnumFilterType.GT:
                            dic_params_query[key_param] = filter_query.value
                            query_builder_partial = query_builder_partial + " " + alias + "." + filter_query.field + \
                                                    " > %(" + key_param + ")s "

                        # " <= "
                        elif filter_type == EnumFilterType.LE:
                            dic_params_query[key_param] = filter_query.value
                            query_builder_partial = query_builder_partial + " " + alias + "." + filter_query.field + \
                                                    " <= %(" + key_param + ")s "

                        # " < "
                        elif filter_type == EnumFilterType.LT:
                            dic_params_query[key_param] = filter_query.value
                            query_builder_partial = query_builder_partial + " " + alias + "." + filter_query.field + \
                                                    " < %(" + key_param + ")s "

                        elif filter_type == EnumFilterType.IN or filter_type == EnumFilterType.NOT_IN:
                            filter_type_in = " IN " if filter_type == EnumFilterType.IN else " NOT IN"
                            query_builder_partial = query_builder_partial + " " + alias + "." + filter_query.field + " "
                            query_builder_partial = query_builder_partial + " " + filter_type_in

                            query_builder_partial = query_builder_partial + "( "
                            first_in_query = True

                            for value_in in filter_query.value:

                                if first_in_query is not True:
                                    query_builder_partial = query_builder_partial + " , "

                                key_param = RFUtilsStr.unique_str()
                                dic_params_query[key_param] = value_in

                                query_builder_partial = query_builder_partial + " %(" + key_param + ")s "
                                first_in_query = False

                            query_builder_partial = query_builder_partial + ") "

                        # closed brackets
                        counter = 0
                        while counter < closed_brackets:
                            counter = counter + 1
                            query_builder_partial = query_builder_partial + " ) "

                        first = False

                query_builder = query_builder + " " + query_builder_partial

        return query_builder_where + " " + query_builder
