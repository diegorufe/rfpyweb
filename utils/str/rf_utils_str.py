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

    @staticmethod
    def split(value, separator):
        """
        Method for split str
        :param value: to split
        :param separator: for apply split
        :return: data split if value is not empty and separator is not None
        """
        ar_response = None
        if RFUtilsStr.is_not_emtpy(value) and separator is not None:
            ar_response = value.split(separator)

        return ar_response
