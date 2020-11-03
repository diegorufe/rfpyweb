from rfpyutils.array.rf_utils_array import RFUtilsArray
from rfpyutils.str.rf_utils_str import RFUtilsStr, DOT
from rfpyweb.transactions.enum_db_engine_type import EnumDbEngineType
from rfpyweb.constants.constants_associations import JOIN_ASSOCIATION_SEPARATOR, FIELD_TABLE_SEPARATOR, DEFAULT_ALIAS
from rfpyweb.constants.query.enum_join_type import EnumJoinType
from rfpyweb.constants.query.enum_filter_type import EnumFilterType
from rfpyweb.constants.query.enum_filter_operation_type import EnumFilterOperationType
from rfpyweb.context.rf_context import RFContext
from rfpyutils.built.rf_utils_built import RFUtilsBuilt
from rfpyweb.constants.query.enum_order_type import EnumOrderType
from rfpyweb.beans.query.limit import Limit
from rfpyweb.core.constants.rf_core_constants import APP_DEFAULT_LIMIT_END_QUERY


class RFUtilsDb:

    @staticmethod
    def get_fields_query(ar_fields=None, rf_transaction=None,
                         db_engine_type: EnumDbEngineType = EnumDbEngineType.RF_MYSQL_POOL, ar_default_fields_table=None):
        """
        Method for get fields to get in queryRF_MYSQL
        :param ar_fields: passed for list function
        :param rf_transaction: to execute query
        :param db_engine_type for database
        :param ar_default_fields_table for table
        :return: ar fields to get in query
        """
        find_all_fields = RFUtilsArray.is_empty(ar_fields)
        ar_fields_query = []

        if db_engine_type == EnumDbEngineType.RF_MYSQL or db_engine_type == EnumDbEngineType.RF_MYSQL_POOL:
            # Find all field raw columns for table
            if find_all_fields and rf_transaction is not None:
                ar_fields_query = ar_default_fields_table
            else:
                ar_fields_query = ar_fields

        return ar_fields_query

    @staticmethod
    def build_select_query(ar_fields_query=None, ar_joins_query=None,
                           db_engine_type: EnumDbEngineType = EnumDbEngineType.RF_MYSQL_POOL, ar_default_fields_table=None,
                           vo_class_name=None):
        """
        Method for build select query
        :param ar_fields_query: to get in query
        :param ar_joins_query: joins for query. Is necessary if has join is fetch
        :param db_engine_type for database
        :param ar_default_fields_table for table
        :param vo_class_name for query
        :return: select query
        """
        query_builder = ""

        # Engine EnumDbEngineType.RF_MYSQL
        if db_engine_type == EnumDbEngineType.RF_MYSQL or db_engine_type == EnumDbEngineType.RF_MYSQL_POOL:
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

                    ar_field = RFUtilsStr.split(field.name, DOT)
                    field_name = field.name
                    field_name_alias = field.name
                    rf_column = None
                    old_vo_class_name = vo_class_name

                    for field_ar in ar_field:
                        rf_column = RFContext.get_column_table(vo_class_name=old_vo_class_name, column_name=field_ar)

                        if rf_column is not None and RFUtilsStr.is_not_emtpy(rf_column.join_table):
                            old_vo_class_name = rf_column.join_vo_class_name
                            field_name = rf_column.column_name
                            field_name_alias = field_name_alias + DOT + rf_column.join_table_column
                        else:
                            break

                    query_builder = query_builder + field_name

                    if RFUtilsStr.is_not_emtpy(field.alias_field):
                        query_builder = query_builder + " " + field.alias_field.strip() + " "
                    else:
                        query_builder = query_builder + " " + \
                                        RFUtilsStr.replace(field_name_alias, DOT, FIELD_TABLE_SEPARATOR) + " "

                    first = False

            # Load all fields
            elif RFUtilsArray.is_not_empty(ar_default_fields_table):
                first = True
                for field in ar_default_fields_table:

                    if not first:
                        query_builder = query_builder + " , "

                    rf_column = RFContext.get_column_table(vo_class_name=vo_class_name, column_name=field.name)

                    if RFUtilsStr.is_empty(rf_column.join_table):
                        query_builder = query_builder + " " + DEFAULT_ALIAS + "." + field.name.strip() + " " + \
                                        RFUtilsStr.replace(field.name.strip(), DOT, FIELD_TABLE_SEPARATOR) + " "
                    else:
                        query_builder = query_builder + " " + DEFAULT_ALIAS + "." + rf_column.join_table_column + " " + \
                                        RFUtilsStr.replace(field.name.strip(), DOT,
                                                           FIELD_TABLE_SEPARATOR) + rf_column.join_table_column + " "

                    first = False

            # Check joins for get data
            if RFUtilsArray.is_not_empty(ar_joins_query):
                # For each join add if join fetch
                ar_joins_fetch = [EnumJoinType.INNER_JOIN_FETCH, EnumJoinType.LEFT_JOIN_FETCH,
                                  EnumJoinType.RIGHT_JOIN_FETCH]

                for join in ar_joins_query:
                    # Add join if fetch for join table. Only join for non alias table by the moment
                    if join.join_type in ar_joins_fetch:
                        old_vo_class_name = vo_class_name
                        ar_join_fields = RFUtilsStr.split(join.field, DOT)

                        for join_field in ar_join_fields:
                            rf_column = RFContext.get_column_table(vo_class_name=old_vo_class_name,
                                                                   column_name=join_field)
                            if rf_column is not None and RFUtilsStr.is_not_emtpy(rf_column.join_table) is True:
                                old_vo_class_name = rf_column.join_vo_class_name

                        ar_rf_columns = RFContext.get_columns_table(old_vo_class_name)

                        field_alias = RFUtilsStr.replace(join.field, DOT, FIELD_TABLE_SEPARATOR)
                        alias = DEFAULT_ALIAS + JOIN_ASSOCIATION_SEPARATOR + RFUtilsStr.replace(join.field, DOT,
                                                                                                JOIN_ASSOCIATION_SEPARATOR)

                        for key_rf_column_apply in ar_rf_columns:
                            rf_column_apply = ar_rf_columns[key_rf_column_apply]
                            query_builder = query_builder + " , "

                            column_name = rf_column_apply.name if RFUtilsStr.is_empty(
                                rf_column_apply.join_table) else rf_column_apply.column_name

                            query_builder = query_builder + " " + alias + "." + column_name + " " + \
                                            field_alias + FIELD_TABLE_SEPARATOR + column_name

                            query_builder = query_builder + " "

        return query_builder

    @staticmethod
    def build_from_query(db_engine_type: EnumDbEngineType = EnumDbEngineType.RF_MYSQL_POOL, table_name: str = None):
        """
        Method for build from query
        :param db_engine_type: for build from
        :param table_name: for from
        :return: from query
        """
        query_builder = ""

        # Engine EnumDbEngineType.RF_MYSQL
        if db_engine_type == EnumDbEngineType.RF_MYSQL or db_engine_type == EnumDbEngineType.RF_MYSQL_POOL:
            query_builder = " FROM " + table_name + " as " + DEFAULT_ALIAS

        return query_builder

    @staticmethod
    def build_joins_query(db_engine_type: EnumDbEngineType = EnumDbEngineType.RF_MYSQL_POOL, ar_joins_query=None,
                          vo_class_name=None):
        """
        Method for build join query
        :param db_engine_type: for build joins
        :param ar_joins_query: to build
        :param vo_class_name for get columns and field
        :return: build whit joins
        """
        query_builder = ""

        if RFUtilsArray.is_not_empty(ar_joins_query):
            for join in ar_joins_query:
                if db_engine_type == EnumDbEngineType.RF_MYSQL or db_engine_type == EnumDbEngineType.RF_MYSQL_POOL:

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

                        join_table = None
                        join_table_field = None
                        ar_join_split_values = RFUtilsStr.split(join.field, DOT)
                        column_name = None
                        alias_join = RFUtilsStr.replace(join.field, DOT, JOIN_ASSOCIATION_SEPARATOR)
                        vo_class_name_join = vo_class_name
                        len_split_values = len(ar_join_split_values) - 1
                        origin_alias_table = DEFAULT_ALIAS

                        for index, join_split_value in enumerate(ar_join_split_values):
                            rf_column = RFContext.get_column_table(vo_class_name=vo_class_name_join,
                                                                   column_name=join_split_value)
                            vo_class_name_join = rf_column.join_vo_class_name
                            join_table = rf_column.join_table
                            join_table_field = rf_column.join_table_column
                            column_name = rf_column.column_name

                            if index != len_split_values:
                                origin_alias_table = origin_alias_table + join_split_value

                        query_builder = query_builder + " " + join_type + " " + join_table

                        if RFUtilsStr.is_not_emtpy(join.alias):

                            query_builder = query_builder + " AS " + join.alias
                            query_builder = query_builder + " ON " + join.alias + "." + join_table_field \
                                            + " = " + origin_alias_table + "." + column_name
                        else:
                            query_builder = query_builder + " AS " + DEFAULT_ALIAS + JOIN_ASSOCIATION_SEPARATOR + \
                                            alias_join + " "
                            query_builder = query_builder + " ON " + DEFAULT_ALIAS + JOIN_ASSOCIATION_SEPARATOR + \
                                            alias_join + "." + join_table_field \
                                            + " = " + origin_alias_table + "." + column_name

        return query_builder

    @staticmethod
    def build_where_query(ar_filters_query=None, dic_params_query={},
                          db_engine_type: EnumDbEngineType = EnumDbEngineType.RF_MYSQL_POOL):
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

                if db_engine_type == EnumDbEngineType.RF_MYSQL or db_engine_type == EnumDbEngineType.RF_MYSQL_POOL:
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

                        field_apply_query = filter_query.field

                        if RFUtilsStr.contains(filter_query.field, DOT):
                            ar_split_values_field = RFUtilsStr.split(filter_query.field, DOT)
                            field_apply_query = ar_split_values_field[-1]
                            ar_split_values_field.pop()
                            alias = DEFAULT_ALIAS
                            for value in ar_split_values_field:
                                alias = alias + JOIN_ASSOCIATION_SEPARATOR + value
                            alias = alias + DOT
                        else:
                            alias = filter_query.alias if RFUtilsStr.is_not_emtpy(filter_query.alias) else DEFAULT_ALIAS
                            alias = alias + (DOT if RFUtilsStr.contains(filter_query.field, DOT) is False else "")

                        key_param = RFUtilsStr.unique_str()

                        # " = "
                        if filter_type == EnumFilterType.EQUAL:
                            dic_params_query[key_param] = filter_query.value
                            query_builder_partial = query_builder_partial + " " + alias + field_apply_query + \
                                                    " =  %(" + key_param + ")s "

                        # " != "
                        elif filter_type == EnumFilterType.DISTINCT:
                            dic_params_query[key_param] = filter_query.value
                            query_builder_partial = query_builder_partial + " " + alias + field_apply_query + \
                                                    " != %(" + key_param + ")s "

                        # " >= "
                        elif filter_type == EnumFilterType.GE:
                            dic_params_query[key_param] = filter_query.value
                            query_builder_partial = query_builder_partial + " " + alias + field_apply_query + \
                                                    " >= %(" + key_param + ")s "

                        # " > "
                        elif filter_type == EnumFilterType.GT:
                            dic_params_query[key_param] = filter_query.value
                            query_builder_partial = query_builder_partial + " " + alias + field_apply_query + \
                                                    " > %(" + key_param + ")s "

                        # " <= "
                        elif filter_type == EnumFilterType.LE:
                            dic_params_query[key_param] = filter_query.value
                            query_builder_partial = query_builder_partial + " " + alias + field_apply_query + \
                                                    " <= %(" + key_param + ")s "

                        # " < "
                        elif filter_type == EnumFilterType.LT:
                            dic_params_query[key_param] = filter_query.value
                            query_builder_partial = query_builder_partial + " " + alias + field_apply_query + \
                                                    " < %(" + key_param + ")s "

                        elif filter_type == EnumFilterType.IN or filter_type == EnumFilterType.NOT_IN:
                            filter_type_in = " IN " if filter_type == EnumFilterType.IN else " NOT IN"
                            query_builder_partial = query_builder_partial + " " + alias + field_apply_query + " "
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

    @staticmethod
    def build_order_query(ar_orders=None, db_engine_type: EnumDbEngineType = EnumDbEngineType.RF_MYSQL_POOL):
        query_builder = ""

        if RFUtilsArray.is_not_empty(ar_orders):

            if db_engine_type == EnumDbEngineType.RF_MYSQL or db_engine_type == EnumDbEngineType.RF_MYSQL_POOL:
                first: bool = True

                query_builder = " ORDER BY "

                for order in ar_orders:
                    if first is not True:
                        query_builder = query_builder + " , "

                    alias = order.alias if RFUtilsStr.is_not_emtpy(order.alias) else DEFAULT_ALIAS

                    ar_split_values = RFUtilsStr.split(order.field, DOT)
                    len_split_values = len(ar_split_values)

                    for index, order_value in enumerate(ar_split_values):

                        if index < len_split_values - 1:
                            alias = alias + JOIN_ASSOCIATION_SEPARATOR + order_value

                    query_builder = query_builder + alias + DOT + ar_split_values.pop() + " " + (
                        "ASC" if order.order_type == EnumOrderType.ASC else "DESC") + " "

                    first = False

        return query_builder

    @staticmethod
    def build_limit(limit, dic_params_query={}):
        """
        Method for build limit
        :param limit: to set in query
        :param dic_params_query: to set star end limit query
        :return: builder with limit
        """
        if limit is None:
            limit = Limit(start=0, end=APP_DEFAULT_LIMIT_END_QUERY)

        start = limit.start if limit.start is not None and limit.start > 0 else 0
        end = limit.end if limit.end is not None and limit.end > 0 else APP_DEFAULT_LIMIT_END_QUERY

        query_builder = " LIMIT  %(limitStart)s , %(limitEnd)s "
        dic_params_query["limitStart"] = start
        dic_params_query["limitEnd"] = end

        return query_builder

    @staticmethod
    def fetch_value_query(vo_class_instance, ar_data):
        """
        Mehtod for fetch data in vo
        :param vo_class_instance: class for vo
        :param ar_data: to fetch
        :return: ar data for fetches values
        """
        ar_response = []
        if ar_data is not None:

            for data in ar_data:

                vo_instance = vo_class_instance()

                for key in data:
                    old_instance = vo_instance
                    ar_key_split = RFUtilsStr.split(key, FIELD_TABLE_SEPARATOR)

                    if RFUtilsArray.is_not_empty(ar_key_split):

                        for field in ar_key_split:
                            # Not use default alias
                            if field == DEFAULT_ALIAS:
                                continue
                            if RFUtilsBuilt.has_attr(old_instance, field):
                                old_tpm_instance = RFUtilsBuilt.get_attr(old_instance, field)

                                if old_tpm_instance is None:
                                    rf_column = RFContext.get_column_table(old_instance.__class__.__name__, field)
                                    if rf_column is not None and RFUtilsStr.is_not_emtpy(
                                            rf_column.join_vo_class_name) is True:
                                        old_tpm_instance = RFContext.instance_vo(
                                            vo_class_name=rf_column.join_vo_class_name)
                                        RFUtilsBuilt.set_attr(old_instance, field, old_tpm_instance)
                                        old_instance = old_tpm_instance
                                    else:
                                        RFUtilsBuilt.set_attr(old_instance, field, data[key])
                                else:
                                    old_instance = old_tpm_instance

                            else:
                                break

                ar_response.append(vo_instance)

        return ar_response

    @staticmethod
    def build_insert_query(vo_instance=None, dic_params_query={}):
        """
        Method for insert build query
        :param table_name: for build insert query
        :param vo_instance: for build insert query
        :param dic_params_query: for build params
        :return: query for insert
        """
        query_builder = "INSERT INTO " + vo_instance.__table_name__ + " "
        query_builder_columns = ""
        query_builder_values = ""

        dic_rf_columns = RFContext.get_columns_table(vo_instance.__class__.__name__)
        first: bool = True

        for key, rf_column in dic_rf_columns.items():

            if rf_column.insertable:

                column_value = None

                if first is not True:
                    query_builder_columns = query_builder_columns + " , "
                    query_builder_values = query_builder_values + " , "

                column_name = rf_column.column_name if RFUtilsStr.is_not_emtpy(rf_column.join_table) else rf_column.name

                query_builder_columns = query_builder_columns + column_name

                if RFUtilsStr.is_not_emtpy(rf_column.join_table):
                    join_instance = RFUtilsBuilt.get_attr(vo_instance, rf_column.name)
                    if join_instance is not None:
                        column_value = RFUtilsBuilt.get_attr(join_instance, rf_column.join_table_column)
                else:
                    column_value = RFUtilsBuilt.get_attr(vo_instance, column_name)

                dic_params_query[column_name] = column_value
                query_builder_values = query_builder_values + " %(" + column_name + ")s "
                first = False

        # Build columns
        query_builder = query_builder + " ( "
        query_builder = query_builder + query_builder_columns
        query_builder = query_builder + " ) "

        # Build values
        query_builder = query_builder + " VALUES ( "
        query_builder = query_builder + query_builder_values
        query_builder = query_builder + " ) "

        return query_builder

    @staticmethod
    def build_update_query(vo_instance=None, dic_params_query={}):
        """
        Method for build update query
        :param vo_instance: to update
        :param dic_params_query: to set update query
        :return:to get build query
        """
        query_builder = "UPDATE " + vo_instance.__table_name__ + " "

        dic_rf_columns = RFContext.get_columns_table(vo_instance.__class__.__name__)
        first: bool = True

        for key, rf_column in dic_rf_columns.items():

            if rf_column.updatable:

                column_value = None

                if first is not True:
                    query_builder = query_builder + " , "
                else:
                    query_builder = query_builder + " SET "

                column_name = rf_column.column_name if RFUtilsStr.is_not_emtpy(rf_column.join_table) else rf_column.name

                if RFUtilsStr.is_not_emtpy(rf_column.join_table):
                    join_instance = RFUtilsBuilt.get_attr(vo_instance, rf_column.name)
                    if join_instance is not None:
                        column_value = RFUtilsBuilt.get_attr(join_instance, rf_column.join_table_column)
                else:
                    column_value = RFUtilsBuilt.get_attr(vo_instance, column_name)

                query_builder = query_builder + " " + column_name + " = "
                dic_params_query[column_name] = column_value
                query_builder = query_builder + " %(" + column_name + ")s "

                first = False

        query_builder = query_builder + " WHERE "

        first: bool = True

        for pk in vo_instance.__ar_pk_fields__:
            if first is not True:
                query_builder = query_builder + " AND "

            column_value = None

            rf_column = RFContext.get_column_table(vo_instance.__class__.__name__, pk)

            column_name = rf_column.column_name if RFUtilsStr.is_not_emtpy(rf_column.join_table) else rf_column.name

            if RFUtilsStr.is_not_emtpy(rf_column.join_table):
                join_instance = RFUtilsBuilt.get_attr(vo_instance, rf_column.name)
                if join_instance is not None:
                    column_value = RFUtilsBuilt.get_attr(join_instance, rf_column.join_table_column)
            else:
                column_value = RFUtilsBuilt.get_attr(vo_instance, column_name)

            query_builder = query_builder + " " + column_name + " = "
            dic_params_query["keyPK_" + pk] = column_value
            query_builder = query_builder + " %(" + "keyPK_" + pk + ")s "

            first = False

        return query_builder
