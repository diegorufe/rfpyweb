"""

  This module contains class for crud routes operations

"""
from rfpyutils.log.rf_utils_logger import RFUtilsLogger

from rfpyweb.core.rf_py_web import RFPyWeb
from rfpyweb.routes.rf_base_route import RFBaseRoute
from rfpyweb.routes.rf_routes_constants import REQUEST_TYPE_POST, TEST_ROUTE, DEFAULT_PATH_REQUEST_ADD, \
    DEFAULT_PATH_REQUEST_DELETE, DEFAULT_PATH_REQUEST_EDIT, DEFAULT_PATH_REQUEST_READ, DEFAULT_PATH_REQUEST_LIST, \
    DEFAULT_PATH_REQUEST_COUNT, DEFAULT_PATH_REQUEST_LOAD_NEW
from rfpyutils.str.rf_utils_str import RFUtilsStr
from rfpyweb.context.rf_context import RFContext
from flask import request
import time
from rfpyweb.core.constants.rf_core_constants import APP_ENABLE_LOG_CRUD_OPERATIONS


class RFBaseCrudRoute(RFBaseRoute):

    def __init__(self, rf_py_web: RFPyWeb, path_requests: str = TEST_ROUTE,
                 path_request_read: str = DEFAULT_PATH_REQUEST_READ,
                 path_request_edit: str = DEFAULT_PATH_REQUEST_EDIT,
                 path_request_delete: str = DEFAULT_PATH_REQUEST_DELETE,
                 path_request_add: str = DEFAULT_PATH_REQUEST_ADD, path_request_list: str = DEFAULT_PATH_REQUEST_LIST,
                 path_request_count: str = DEFAULT_PATH_REQUEST_COUNT,
                 path_request_load_new: str = DEFAULT_PATH_REQUEST_LOAD_NEW,
                 secure: bool = True, service_name: str = None):
        # Call super constructor
        RFBaseRoute.__init__(self, rf_py_web, path_requests=path_requests)
        self.path_request_read = path_request_read
        self.path_request_edit = path_request_edit
        self.path_request_delete = path_request_delete
        self.path_request_add = path_request_add
        self.path_request_list = path_request_list
        self.path_request_count = path_request_count
        self.path_request_load_new = path_request_load_new
        self.secure = secure
        self.service = None

        if RFUtilsStr.is_not_emtpy(service_name):
            self.service = RFContext.get_service(service_name)

    def __routes__(self):
        RFBaseRoute.__routes__(self)

        @self.rf_py_web.route(self.path_requests + self.path_request_read,
                              endpoint=self.path_requests + self.path_request_read, methods=[REQUEST_TYPE_POST])
        @self.rf_py_web.secure_filter_decorator(self.path_requests + self.path_request_read)
        def read_request():
            """
            Method for listen read request
            :return:
            """
            return self.read(data_request=request.json, params=None)

        @self.rf_py_web.route(self.path_requests + self.path_request_list,
                              endpoint=self.path_requests + self.path_request_list, methods=[REQUEST_TYPE_POST])
        @self.rf_py_web.secure_filter_decorator(self.path_requests + self.path_request_list)
        def list_request():
            """
            Method for listen list request
            :return:
            """
            return self.list(data_request=request.json, params=None)

        @self.rf_py_web.route(self.path_requests + self.path_request_count,
                              endpoint=self.path_requests + self.path_request_count, methods=[REQUEST_TYPE_POST])
        @self.rf_py_web.secure_filter_decorator(self.path_requests + self.path_request_count)
        def count_request():
            """
            Method for listen read request
            :return:
            """
            return self.count(data_request=request.json, params=None)

        @self.rf_py_web.route(self.path_requests + self.path_request_add,
                              endpoint=self.path_requests + self.path_request_add, methods=[REQUEST_TYPE_POST])
        @self.rf_py_web.secure_filter_decorator(self.path_requests + self.path_request_add)
        def add_request():
            """
            Method for listen add request
            :return:
            """
            return self.add(data_request=request.json, params=None)

        @self.rf_py_web.route(self.path_requests + self.path_request_edit,
                              endpoint=self.path_requests + self.path_request_edit, methods=[REQUEST_TYPE_POST])
        @self.rf_py_web.secure_filter_decorator(self.path_requests + self.path_request_edit)
        def edit_request():
            """
            Method for listen edit request
            :return:
            """
            return self.edit(data_request=request.json, params=None)

        @self.rf_py_web.route(self.path_requests + self.path_request_delete,
                              endpoint=self.path_requests + self.path_request_delete, methods=[REQUEST_TYPE_POST])
        @self.rf_py_web.secure_filter_decorator(self.path_requests + self.path_request_delete)
        def delete_request():
            """
            Method for listen delete request
            :return:
            """
            return self.delete(data_request=request.json, params=None)

        @self.rf_py_web.route(self.path_requests + self.path_request_load_new,
                              endpoint=self.path_requests + self.path_request_load_new, methods=[REQUEST_TYPE_POST])
        @self.rf_py_web.secure_filter_decorator(self.path_requests + self.path_request_load_new)
        def load_new_request():
            """
            Method for listen edit request
            :return:
            """
            return self.load_new(params=None)

    def read(self, data_request=None, params=None):
        """
        Method for read data vo with pk values
        :param data_request: data receive in request.
        :param params: params pass method
        :return: vo read by pk values
        """
        ar_pks_values = self.json_value(data_request, 'pkValues')
        ar_joins_request = self.json_value(data_request, 'joins')
        vo = self.service.read(ar_pks_values, ar_joins=self.make_joins_request(ar_joins_request))
        return self.make_json_response(data_json=vo, status=self.status_ok())

    def list(self, data_request=None, params=None):
        """
        Method for list data
        :param data_request: data receive in request.
        :param params: params pass method
        :return: list of data
        """
        start_time_ns = 0
        if APP_ENABLE_LOG_CRUD_OPERATIONS:
            start_time_ns = time.time_ns()

        ar_fields_request = self.json_value(data_request, 'fields')
        ar_joins_request = self.json_value(data_request, 'joins')
        ar_filters_request = self.json_value(data_request, 'filters')
        ar_orders_request = self.json_value(data_request, 'orders')
        limit_request = self.json_value(data_request, 'limit')
        data = self.service.list(
            ar_fields=self.make_fields_request(ar_fields_request),
            ar_filters=self.make_filters_request(ar_filters_request),
            ar_joins=self.make_joins_request(ar_joins_request),
            ar_orders=self.make_orders_request(ar_orders_request),
            limit=self.make_limit_request(limit_request)
        )

        if APP_ENABLE_LOG_CRUD_OPERATIONS:
            time_ns = time.time_ns() - start_time_ns
            RFUtilsLogger.debug(
                "$$Time crud list before json: " + str(time_ns) + ", ms " + str(
                    time_ns / 1000000))

        return self.make_json_response(data_json=data, status=self.status_ok(), start_time_ns=start_time_ns)

    def count(self, data_request=None, params=None):
        """
        Method for count data
        :param data_request: data receive in request.
        :param params: params pass method
        :return: count of data
        """
        ar_joins_request = data_request['joins']
        ar_filters_request = data_request['filters']
        data = self.service.count(ar_filters=self.make_filters_request(ar_filters_request),
                                  ar_joins=self.make_joins_request(ar_joins_request))
        return self.make_json_response(data_json=data, status=self.status_ok())

    def add(self, data_request=None, params=None):
        """
        Method for add data in request
        :param data_request: data receive in request.
        :param params: params pass method
        :return: data added
        """
        vo_request_data = data_request['data']
        data = self.service.add(vo=self.json_data_to_vo(self.service.vo_class_name(), vo_request_data))
        return self.make_json_response(data_json=data, status=self.status_created())

    def edit(self, data_request=None, params=None):
        """
        Method for edit data
        :param data_request: data receive in request.
        :param params: params pass method
        :return: data edited
        """
        vo_request_data = data_request['data']
        data = self.service.edit(vo=self.json_data_to_vo(self.service.vo_class_name(), vo_request_data))
        return self.make_json_response(data_json=data, status=self.status_ok())

    def delete(self, data_request=None, params=None):
        """
        Method for delete data
        :param data_request: data receive in request.
        :param params: params pass method
        :return: True deleted False if not
        """
        ar_pks_values = data_request['pkValues']
        data = self.service.delete(ar_pks_values)
        return self.make_json_response(data_json=data, status=self.status_ok())

    def load_new(self, params=None):
        """
        Method for load new vo
        :param params:
        :return:
        """
        vo = self.service.new_instance_vo()
        return self.make_json_response(data_json=vo, status=self.status_ok())
