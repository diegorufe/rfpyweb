from rfpyweb.constants.query.enum_order_type import EnumOrderType


class Order:

    def __init__(self, field: str = None, alias: str = None, order_type: EnumOrderType = EnumOrderType.ASC):
        """
        Class for build order in query
        :param field: to order
        :param alias: to order
        :param order_type: for order
        """
        self.field = field
        self.alias = alias
        self.order_type = order_type
