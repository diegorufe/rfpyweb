from transactions.enum_db_engine_type import EnumDbEngineType
from utils.str.rf_utils_str import RFUtilsStr
from transactions.rf_transaction_manager import RFTransactionManager
from db.rf_db_tables_information import RFDbTableInformation

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
            dic_columns = _dic_db_tables_information[vo_class_name]

        return dic_columns

    @staticmethod
    def add_table(vo_class_name):
        """
        Method for add table to context
        :param vo_class_name: for mapping data
        :return: None
        """
        if vo_class_name is not None:
            _dic_db_tables_information[vo_class_name] = RFDbTableInformation(vo_class_name)

    @staticmethod
    def add_column_table(class_vo_name: str = None, rf_column=None):
        """
        Method for add column table
        :param class_vo_name: for add column
        :param rf_column: to add
        :return: None
        """
        if RFUtilsStr.is_not_emtpy(
                class_vo_name) and class_vo_name in _dic_db_tables_information and rf_column is not None:
            _dic_db_tables_information[class_vo_name].add_column(rf_column)

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
