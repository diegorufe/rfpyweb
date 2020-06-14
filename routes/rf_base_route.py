"""

   This module contains class for routes operations

"""
from core.rf_py_web import RFPyWeb
from routes.rf_rourtes_constants import DEFAULT_PATH_REQUEST_TEST, REQUEST_TYPE_GET, TEST_ROUTE


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
            return self.rf_py_web.json(test="Test")
