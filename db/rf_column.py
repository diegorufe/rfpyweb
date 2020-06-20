class RFColumn:

    def __init__(self, name: str = None, column_name: str = None,
                 join_table: str = None, join_vo_class_name: str = None,
                 join_table_column: str = 'id', insertable: bool = True, updatable: bool = True):
        """
        Constructor for class rf_column
        :param name: for column
        :param column_name: for column in database
        :param join_table: for joins reference
        :param join_vo_class_name: for join reference
        :param join_table_column: for joins reference
        :param insertable: indicate insertable for database
        :param updatable: indicate updatable for database
        """
        self.name = name
        self.column_name = column_name
        self.join_table = join_table
        self.join_vo_class_name = join_vo_class_name
        self.join_table_column = join_table_column
        self.insertable = insertable
        self.updatable = updatable
