import datetime
from decimal import Decimal


def rf_data_to_json_converter(data):
    """
    Json converter for data
    :param data: to convert
    :return: data converted
    """
    result = None

    if isinstance(data, datetime.datetime) or isinstance(data, Decimal):
        result = data.__str__()
    elif isinstance(data, bytes):
        result = data.decode("utf-8")
    else:
        result = data.__dict__

    return result
