"""
  Response for bo operations
"""


class RFResponseDao:

    def __init__(self, data=None, code_error=0, message_error=None):
        """
        Constructor for class response dao
        :param data: response dao if not fail
        :param code_error: for error response dao
        :param message_error: for error response
        """
        self.data = data
        self.code_error = code_error
        self.message_error = message_error
