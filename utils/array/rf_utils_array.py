"""
Utilities for array
"""
import numpy as np


class RFUtilsArray:

    @staticmethod
    def is_not_empty(array):
        """
        Method to check array is not empty.
        :param array: to check
        :return: True if array is not None isinstance (list, tuple, np.ndarray) and len > 0
        """
        return array is not None and isinstance(array, (list, tuple, np.ndarray)) and len(array) > 0

    @staticmethod
    def is_empty(array):
        """
        Method to check array is empty
        :param array: to check
        :return: True if is None not instance (list, tuple, np.ndarray) or len = 0
        """
        return RFUtilsArray.is_not_empty(array) is False
