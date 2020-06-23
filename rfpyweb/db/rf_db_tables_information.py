class RFDbTableInformation:

    def __init__(self, class_vo: None):
        """
        Constructor for class RFDbTableInformation
        """
        self.class_vo = class_vo
        self.table_name = class_vo.__table_name__
        self.__dic_table_columns = {}

    def add_column(self, rf_column):
        """
        Method for add column for db table information
        :param rf_column: to add
        :return: None
        """
        if rf_column is not None:
            self.__dic_table_columns[rf_column.name] = rf_column

    def get_columns(self):
        """
        Method for get columns for table information
        :return: dic table columns information
        """
        return self.__dic_table_columns

    def instance(self):
        """
        Method for instance vo
        :return: vo
        """
        return self.class_vo()
