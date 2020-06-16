"""

  This module contains class for crud routes operations

"""
from core.rf_py_web import RFPyWeb
from routes.rf_base_route import RFBaseRoute
from routes.rf_rourtes_constants import REQUEST_TYPE_POST, REQUEST_TYPE_GET, TEST_ROUTE, DEFAULT_PATH_REQUEST_ADD, \
    DEFAULT_PATH_REQUEST_DELETE, DEFAULT_PATH_REQUEST_EDIT, DEFAULT_PATH_REQUEST_READ, DEFAULT_PATH_REQUEST_LIST
from utils.str.rf_utils_str import RFUtilsStr
from context.rf_context import RFContext


class RFBaseCrudRoute(RFBaseRoute):

    def __init__(self, rf_py_web: RFPyWeb, path_requests: str = TEST_ROUTE,
                 path_request_read: str = DEFAULT_PATH_REQUEST_READ,
                 path_request_edit: str = DEFAULT_PATH_REQUEST_EDIT,
                 path_request_delete: str = DEFAULT_PATH_REQUEST_DELETE,
                 path_request_add: str = DEFAULT_PATH_REQUEST_ADD, path_request_list: str = DEFAULT_PATH_REQUEST_LIST,
                 secure: bool = True, service_name: str = None):
        # Call super constructor
        RFBaseRoute.__init__(self, rf_py_web, path_requests=path_requests)
        self.path_request_read = path_request_read
        self.path_request_edit = path_request_edit
        self.path_request_delete = path_request_delete
        self.path_request_add = path_request_add
        self.path_request_list = path_request_list
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
            :return: None
            """
            return self.read()

        @self.rf_py_web.route(self.path_requests + self.path_request_list,
                              endpoint=self.path_requests + self.path_request_list, methods=[REQUEST_TYPE_GET])
        @self.rf_py_web.secure_filter_decorator(self.path_requests + self.path_request_list)
        def list_request():
            """
            Method for listen read request
            :return: None
            """
            return self.list()

    def read(self):
        """
        Method for execute read crud operation
        :return: response json
        """
        return self.rf_py_web.json(test="Read")

    def list(self):
        response = None
        response_bo = None
        if self.service is not None:
            response_bo = self.service.list()

        if response_bo is not None:
            response = self.rf_py_web.json(response_bo)

        return response
