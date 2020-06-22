"""

   This module contains class for routes operations

"""
from core.rf_py_web import RFPyWeb
from routes.rf_rourtes_constants import DEFAULT_PATH_REQUEST_TEST, REQUEST_TYPE_GET, TEST_ROUTE
from constants.http.enum_http_status_types import EnumHttpStatusType
from utils.array.rf_utils_array import RFUtilsArray
from beans.query.join import Join
from constants.query.enum_join_type import EnumJoinType
from constants.query.enum_filter_type import EnumFilterType
from constants.query.enum_filter_operation_type import EnumFilterOperationType
from constants.query.enum_order_type import EnumOrderType
from beans.query.filter import Filter
from beans.query.order import Order
from beans.query.limit import Limit
from beans.query.field import Field
from collections.abc import Mapping
from context.rf_context import RFContext
from utils.built.rf_utils_built import RFUtilsBuilt


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
        return self.jsonify(data=data_json, status=status, mimetype='application/json')

    def json(self, data):
        """
        Method for convert data to json.
        :param data to convert
        :return: data convert to json
        """
        return self.rf_py_web(data)

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
                ar_joins.append(Join(field=join_request.field, join_type=EnumJoinType.convert(join_request.joinType),
                                     alias=join_request.alias, custom_query_join=join_request.customQueryJoin))

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
                ar_filters.append(Filter(field=filter_request.field, alias=filter_request.alias,
                                         filter_type=EnumFilterType.convert(filter_request.filterType),
                                         value=filter_request.value,
                                         filter_operation_type=EnumFilterOperationType.convert(
                                             filter_request.filterOperationType),
                                         open_brackets=filter_request.openBrackets,
                                         closed_brackets=filter_request.closeBrackets))
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
                ar_orders.append(Order(field=order_request.field, alias=order_request.alias,
                                       order_type=EnumOrderType.convert(order_request.orderType)))

        return ar_orders

    def make_limit_request(self, limit_request):
        """
        Method for make limit request
        :param limit_request: to make
        :return: limit
        """
        limit = None
        if limit_request is not None:
            limit = Limit(start=limit_request.start, end=limit_request.end)
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
                ar_fields.append(Field(name=field_request.name, alias_table=field_request.aliasTable,
                                       alias_field=field_request.aliasField, custom_field=field_request.customField))

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
                    else:
                        RFUtilsBuilt.set_attr(vo_instance, key, data_vo)

        return vo_instance
