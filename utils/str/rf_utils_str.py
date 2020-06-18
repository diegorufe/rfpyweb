"""
Utilities for str
"""
import uuid


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
        return RFUtilsStr.is_not_emtpy(value) is False

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

    @staticmethod
    def unique_str(time_execute: int = 1):
        """
        Method for generate unique str
        :param time_execute for exeucte concat unique str
        :return: unique str
        """
        unique = ""
        counter: int = 0

        if time_execute is None or time_execute < 0:
            time_execute = 1

        while counter < time_execute:
            counter = counter + 1
            unique = unique + uuid.uuid4().hex.upper()

        return unique
