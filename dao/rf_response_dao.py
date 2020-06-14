"""
  Response for dao operations
"""


class RFResponseDao:

    def __init__(self, dto=None, code_error=0, message_error=None):
        """
        Constructor for class response dao
        :param dto: response dao if not fail
        :param code_error: for error response dao
        :param message_error: for error response
        """
        self.dto = dto
        self.code_error = code_error
        self.message_error = message_error
