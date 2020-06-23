import json
import logging.config, logging
import os


class RFLogger:

    @staticmethod
    def init_log(json_config: str = os.path.dirname(os.path.abspath(__file__)) + '/logging.json'):
        """
        Method for init log
        :param json_config:
        :return:
        """
        with open(json_config) as json_file:
            data = json.load(json_file)
        logging.config.dictConfig(data)

    @staticmethod
    def error(msg: str, *args, **kwargs):
        """
        Method to send error log
        :param msg:
        :param args:
        :param kwargs:
        :return:
        """
        logging.error(msg, *args, **kwargs)

    @staticmethod
    def debug(msg: str, *args, **kwargs):
        """
        Method to send debug message
        :param msg:
        :param args:
        :param kwargs:
        :return:
        """
        logging.debug(msg, *args, **kwargs)
