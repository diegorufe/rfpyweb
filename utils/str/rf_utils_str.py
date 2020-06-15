"""
Utilities for str
"""


class RFUtilsStr:

    @staticmethod
    def is_not_emtpy(value):
        """
        Method to check value is not empty
        :param value: to check
        :return: True if value is not None and isinstance str and strip() != ""
        """
        return value is not None and isinstance(value, str) and value.strip() != ""

    @staticmethod
    def is_empty(value):
        """
        Method to check value is empty
        :param value: to check
        :return: True if value is None or non instance of str or value.strip() == ""
        """
        return RFUtilsStr.is_not_emtpy(value) is not False
