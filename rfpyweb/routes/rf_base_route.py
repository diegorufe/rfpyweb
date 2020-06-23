"""

   This module contains class for routes operations

"""
from rfpyweb.core.rf_py_web import RFPyWeb
from rfpyweb.routes.rf_routes_constants import DEFAULT_PATH_REQUEST_TEST, REQUEST_TYPE_GET, TEST_ROUTE
from rfpyweb.constants.http.enum_http_status_types import EnumHttpStatusType
from rfpyutils.array.rf_utils_array import RFUtilsArray
from rfpyweb.beans.query.join import Join
from rfpyweb.constants.query.enum_join_type import EnumJoinType
from rfpyweb.constants.query.enum_filter_type import EnumFilterType
from rfpyweb.constants.query.enum_filter_operation_type import EnumFilterOperationType
from rfpyweb.constants.query.enum_order_type import EnumOrderType
from rfpyweb.beans.query.filter import Filter
from rfpyweb.beans.query.order import Order
from rfpyweb.beans.query.limit import Limit
from rfpyweb.beans.query.field import Field
from collections.abc import Mapping
from rfpyweb.context.rf_context import RFContext
from rfpyutils.built.rf_utils_built import RFUtilsBuilt
from decimal import Decimal


class RFBaseRoute:

    def __init__(self, rf_py_web: RFPyWeb, path_requests: str = TEST_ROUTE):
        """
        Base constructor for route request operations
        :param rf_py_web: is class launch and configure web application
        :param path_requests: is path for request operations
        """
        self.rf_py_web = rf_py_web
        self.path_requests = path_requests
        self._path_request_test = DEFAULT_PATH_REQUEST_TEST

    def load(self):
        """
        Method for load config for route
        :return: None
        """
        self.__routes__()

    def __routes__(self):
        """
        Method for create routes for request operations
        :return: None
        """

        @self.rf_py_web.route(self.path_requests + self._path_request_test,
                              endpoint=self.path_requests + self._path_request_test, methods=[REQUEST_TYPE_GET])
        def test_route():
            """
            Method for create test request operations
            :return: {test: 'Test'}
            """
            return self.jsonify(test="Test")

    def make_json_response(self, data_json, status: EnumHttpStatusType = EnumHttpStatusType.BAD_REQUEST):
        """
        Method for make json response
        :param data_json: to convert
        :param status: to send
        :return: json response
        """
        return self.jsonify(data=data_json, status=status.value, mimetype='application/json')

    def json(self, data):
        """
        Method for convert data to json.
        :param data to convert
        :return: data convert to json
        """
        return self.rf_py_web.json(data)

    def jsonify(self, *args, **kwargs):
        """
        jsonify data
        :param args:
        :param kwargs:
        :return: json for data
        """
        return self.rf_py_web.jsonify(*args, **kwargs)

    def status_ok(self):
        """
        Method for get status ok
        :return: status ok
        """
        return EnumHttpStatusType.OK

    def status_bad_request(self):
        """
        Method for get status bad request
        :return: status bad request
        """
        return EnumHttpStatusType.BAD_REQUEST

    def status_created(self):
        """
        Method for get status created
        :return: status created
        """
        return EnumHttpStatusType.CREATED

    def status_unauthorized(self):
        """
        Method for get status unauthorized
        :return: status unauthorized
        """
        return EnumHttpStatusType.UNAUTHORIZED

    def make_joins_request(self, ar_joins_request):
        """
        Method for conver join request to joins query
        :param ar_joins_request: to convert
        :return: ar_joins for request
        """
        ar_joins = []

        if RFUtilsArray.is_not_empty(ar_joins_request):

            for join_request in ar_joins_request:
                ar_joins.append(Join(field=self.json_value(join_request, 'field'),
                                     join_type=EnumJoinType.convert(self.json_value(join_request, 'joinType')),
                                     alias=self.json_value(join_request, 'alias'),
                                     custom_query_join=self.json_value(join_request, 'customQueryJoin')))

        return ar_joins

    def make_filters_request(self, ar_filters_request):
        """
        Method for make filters request
        :param ar_filters_request: to make
        :return: ar filters make
        """
        ar_filters = []
        if RFUtilsArray.is_not_empty(ar_filters_request):

            for filter_request in ar_filters_request:
                ar_filters.append(Filter(field=self.json_value(filter_request, 'field'),
                                         alias=self.json_value(filter_request, 'alias'),
                                         filter_type=EnumFilterType.convert(
                                             self.json_value(filter_request, 'filterType')),
                                         value=self.json_value(filter_request, 'value'),
                                         filter_operation_type=EnumFilterOperationType.convert(
                                             self.json_value(filter_request, 'filterOperationType')),
                                         open_brackets=self.json_value(filter_request, 'openBrackets'),
                                         closed_brackets=self.json_value(filter_request, 'closeBrackets')))
        return ar_filters

    def make_orders_request(self, ar_orders_request):
        """
        Method for make orders request
        :param ar_orders_request: to make
        :return: ar orders make
        """
        ar_orders = []

        if RFUtilsArray.is_not_empty(ar_orders_request):

            for order_request in ar_orders_request:
                ar_orders.append(
                    Order(field=self.json_value(order_request, 'field'), alias=self.json_value(order_request, 'alias'),
                          order_type=EnumOrderType.convert(self.json_value(order_request, 'orderType'))))

        return ar_orders

    def make_limit_request(self, limit_request):
        """
        Method for make limit request
        :param limit_request: to make
        :return: limit
        """
        limit = None
        if limit_request is not None:
            limit = Limit(start=self.json_value(limit_request, 'start'), end=self.json_value(limit_request, 'end'))
        return limit

    def make_fields_request(self, ar_fields_request):
        """
        Method for make fields request
        :param ar_fields_request: to make
        :return: fields request
        """
        ar_fields = []

        if RFUtilsArray.is_not_empty(ar_fields_request):
            for field_request in ar_fields_request:
                ar_fields.append(
                    Field(name=self.json_value(field_request, 'name'),
                          alias_table=self.json_value(field_request, 'aliasTable'),
                          alias_field=self.json_value(field_request, 'aliasField'),
                          custom_field=self.json_value(field_request, 'customField')))

        return ar_fields

    def json_data_to_vo(self, vo_class_name, data):
        """
        Mehtod for fetch data in vo
        :param vo_class_name: class name for vo
        :param ar_data: to fetch
        :return: ar data for fetches values
        """

        vo_instance = RFContext.instance_vo(vo_class_name)

        if data is not None:
            for key, data_vo in data.items():
                rf_column = RFContext.get_column_table(vo_class_name, key)

                if data_vo is not None and rf_column is not None:
                    if isinstance(data_vo, Mapping):
                        RFUtilsBuilt.set_attr(vo_instance, key,
                                              self.json_data_to_vo(rf_column.join_vo_class_name, data_vo))
                    elif isinstance(data_vo, float):
                        RFUtilsBuilt.set_attr(vo_instance, key, Decimal(data_vo))
                    else:
                        RFUtilsBuilt.set_attr(vo_instance, key, data_vo)

        return vo_instance

    def json_value(self, json_data, key):
        """
        Method for get json value
        :param json_data: to get value
        :param key: to get value
        :return: get key value
        """
        result = None
        if json_data is not None and key is not None and key in json_data:
            return json_data[key]
        return result
