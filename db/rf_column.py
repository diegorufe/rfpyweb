class RFColumn:

    def __init__(self, name: str = None, join_property_name: str = None, join_column: str = None,
                 join_table: str = None, join_vo_class_name: str = None,
                 join_table_column: str = 'id'):
        """
        Constructor for class rf_column
        :param name: for column
        :param join_column: for joins reference
        :param join_property_name for join property vo
        :param join_table: for joins reference
        :param join_vo_class_name: for join reference
        :param join_table_column: for joins reference
        """
        self.name = name
        self.join_property_name = join_property_name
        self.join_column = join_column
        self.join_table = join_table
        self.join_vo_class_name = join_vo_class_name
        self.join_table_column = join_table_column
