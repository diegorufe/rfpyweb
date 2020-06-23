from rfpyweb.transactions.enum_db_engine_type import EnumDbEngineType
from rfpyutils.str.rf_utils_str import RFUtilsStr
from rfpyweb.transactions.rf_transaction_manager import RFTransactionManager
from rfpyweb.db.rf_db_tables_information import RFDbTableInformation

_dic_db_engines = {}
_dic_services = {}
_rf_transaction_manager = None
_dic_db_tables_information = {}


class RFContext:

    @staticmethod
    def add_service(key, service):
        """
        Method for add service. Only add if key is not none and service is not none and key dont find in service
        :param key: to add service
        :param service: to add
        :return: None
        """
        if key is not None and service is not None and key not in _dic_services:
            _dic_services[key] = service

    @staticmethod
    def get_service(key):
        """
        Method for get service
        :param key: for get service
        :return: service if found by key else return None
        """
        service = None
        if key is not None and key in _dic_services:
            service = _dic_services[key]
        return service

    @staticmethod
    def add_db_engine(key: EnumDbEngineType, db_engine):
        """
        Method for add db engine. This method only add db_engine if not None and key not None
        :param key: for db engine
        :param db_engine: to add
        :return: None
        """
        if key is not None and db_engine is not None:
            _dic_db_engines[key] = db_engine

    @staticmethod
    def get_db_engine(key: EnumDbEngineType):
        """
        Method for get db engine by key. If key is None or dont find engine return None
        :param key: for get db engine
        :return: db engine if found else return None
        """
        db_engine = None
        if key is not None and key in _dic_db_engines:
            db_engine = _dic_db_engines[key]
        return db_engine

    @staticmethod
    def get_columns_table(vo_class_name: str = None):
        """
        Method for get fields for table
        :param vo_class_name: is a name for table to get columns
        :return: map columns for table
        """
        dic_columns = {}

        if RFUtilsStr.is_not_emtpy(vo_class_name) and vo_class_name in _dic_db_tables_information:
            dic_columns = _dic_db_tables_information[vo_class_name].get_columns()

        return dic_columns

    @staticmethod
    def get_column_table(vo_class_name: str = None, column_name: str = None):
        """
        Method for get column for table
        :param vo_class_name: is a name for table to get columns
        :param column_name column name for get
        :return: column for table
        """
        rf_column = None

        if RFUtilsStr.is_not_emtpy(vo_class_name) and RFUtilsStr.is_not_emtpy(
                column_name) and vo_class_name in _dic_db_tables_information:
            dic_columns = _dic_db_tables_information[vo_class_name].get_columns()

            if dic_columns is not None and column_name in dic_columns:
                rf_column = dic_columns[column_name]

        return rf_column

    @staticmethod
    def add_table(vo_class_name):
        """
        Method for add table to context
        :param vo_class_name: for mapping data
        :return: None
        """
        if vo_class_name is not None:
            _dic_db_tables_information[vo_class_name.__name__] = RFDbTableInformation(vo_class_name)

    @staticmethod
    def add_column_table(vo_class_name: str = None, rf_column=None):
        """
        Method for add column table
        :param vo_class_name: for add column
        :param rf_column: to add
        :return: None
        """
        if RFUtilsStr.is_not_emtpy(
                vo_class_name) and vo_class_name in _dic_db_tables_information and rf_column is not None:
            _dic_db_tables_information[vo_class_name].add_column(rf_column)

    @staticmethod
    def get_transaction_manager():
        """
        Method for get transaction manager
        :return: transaction manager
        """
        global _rf_transaction_manager
        if _rf_transaction_manager is None:
            _rf_transaction_manager = RFTransactionManager()
        return _rf_transaction_manager

    @staticmethod
    def instance_vo(vo_class_name: str = None):
        """
        Method for instance vo
        :param vo_class_name: for get instance
        :return: instance vo if find
        """
        instance = None
        if vo_class_name is not None and vo_class_name in _dic_db_tables_information:
            instance = _dic_db_tables_information[vo_class_name].instance()
        return instance
