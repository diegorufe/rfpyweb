from utils.array.rf_utils_array import RFUtilsArray
from utils.str.rf_utils_str import RFUtilsStr
from transactions.enum_db_engine_type import EnumDbEngineType
from constants.constants_associations import JOIN_ASSOCIATION_SEPARATOR, FIELD_TABLE_SEPARATOR, DEFAULT_ALIAS
from constants.enum_join_type import EnumJoinType
from constants.enum_filter_type import EnumFilterType
from constants.enum_filter_operation_type import EnumFilterOperationType


class RFUtilsDb:

    @staticmethod
    def get_fields_query(ar_fields=None, rf_transaction=None,
                         db_engine_type: EnumDbEngineType = EnumDbEngineType.RF_MYSQL, ar_default_fields_table=None):
        """
        Method for get fields to get in query
        :param ar_fields: passed for list function
        :param rf_transaction: to execute query
        :param db_engine_type for database
        :param ar_default_fields_table for table
        :return: ar fields to get in query
        """
        find_all_fields = RFUtilsArray.is_empty(ar_fields)
        ar_fields_query = []

        if db_engine_type == EnumDbEngineType.RF_MYSQL:
            # Find all field raw columns for table
            if find_all_fields and rf_transaction is not None:
                ar_fields_query = ar_default_fields_table
            else:
                ar_fields_query = ar_fields

        return ar_fields_query

    @staticmethod
    def build_select_query(ar_fields_query=None, ar_joins_query=None,
                           db_engine_type: EnumDbEngineType = EnumDbEngineType.RF_MYSQL, ar_default_fields_table=None):
        """
        Method for build select query
        :param ar_fields_query: to get in query
        :param ar_joins_query: joins for query. Is necessary if has join is fetch
        :param db_engine_type for database
        :param ar_default_fields_table for table
        :return: select query
        """
        query_builder = ""

        # Engine EnumDbEngineType.RF_MYSQL
        if db_engine_type == EnumDbEngineType.RF_MYSQL:
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
                        query_builder = query_builder + " " + DEFAULT_ALIAS + "."

                    query_builder = query_builder + field.name.strip()

                    if RFUtilsStr.is_not_emtpy(field.alias_field):
                        query_builder = query_builder + " " + field.alias_field.strip() + " "
                    else:
                        query_builder = query_builder + " " + \
                                        field.name.strip() + " "

                    first = False

            # Load all fields
            elif RFUtilsArray.is_not_empty(ar_default_fields_table):
                first = True
                for field in ar_default_fields_table:
                    if not first:
                        query_builder = query_builder + " , "
                    query_builder = query_builder + " " + DEFAULT_ALIAS + "." + field.name.strip() + " " + \
                                    RFUtilsStr.replace(field.name.strip(), ".", FIELD_TABLE_SEPARATOR) + " "

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
                        pass
                        # ar_fields_join = RFContext.get_fields_table(join.join_table, self.db_engine_type)
                        # if RFUtilsArray.is_not_empty(ar_fields_join):
                        #     for field in ar_fields_join:
                        #         query_builder = query_builder + ", " + self._table_name + \
                        #                         JOIN_ASSOCIATION_SEPARATOR + join.join_field + "." + field.name \
                        #                         + "  " + self._table_name \
                        #                         + JOIN_ASSOCIATION_SEPARATOR + join.join_field \
                        #                         + FIELD_TABLE_SEPARATOR + field.name

        return query_builder

    @staticmethod
    def build_from_query(db_engine_type: EnumDbEngineType = EnumDbEngineType.RF_MYSQL, table_name: str = None):
        """
        Method for build from query
        :param db_engine_type: for build from
        :param table_name: for from
        :return: from query
        """
        query_builder = ""

        # Engine EnumDbEngineType.RF_MYSQL
        if db_engine_type == EnumDbEngineType.RF_MYSQL:
            query_builder = " FROM " + table_name + " as " + DEFAULT_ALIAS

        return query_builder

    @staticmethod
    def build_joins_query(db_engine_type: EnumDbEngineType = EnumDbEngineType.RF_MYSQL, ar_joins_query=None):
        """
        Method for build join query
        :param db_engine_type: for build joins
        :param ar_joins_query: to build
        :return: build whit joins
        """
        query_builder = ""

        if RFUtilsArray.is_not_empty(ar_joins_query):
            for join in ar_joins_query:
                if db_engine_type == EnumDbEngineType.RF_MYSQL:

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
                                            + " = " + DEFAULT_ALIAS + "." + join.join_field
                        else:
                            query_builder = query_builder + " AS " + DEFAULT_ALIAS + JOIN_ASSOCIATION_SEPARATOR + \
                                            join.join_field + " "
                            query_builder = query_builder + " ON " + DEFAULT_ALIAS + JOIN_ASSOCIATION_SEPARATOR + \
                                            join.join_field + "." + join.join_table_field \
                                            + " = " + DEFAULT_ALIAS + "." + join.join_table_field

        return query_builder

    @staticmethod
    def build_where_query(ar_filters_query=None, dic_params_query={},
                          db_engine_type: EnumDbEngineType = EnumDbEngineType.RF_MYSQL):
        """
        Method for build where query
        :param ar_filters_query: to build
        :param dic_params_query: to set in query
        :param db_engine_type: to build
        :return: where build
        """
        query_builder = ""
        query_builder_where = ""

        if RFUtilsArray.is_not_empty(ar_filters_query):

            first: bool = True

            for filter_query in ar_filters_query:

                query_builder_partial = ""

                if db_engine_type == EnumDbEngineType.RF_MYSQL:
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

                        alias = filter_query.alias if RFUtilsStr.is_not_emtpy(filter_query.alias) else DEFAULT_ALIAS
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
