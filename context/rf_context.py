from transactions.enum_db_engine_type import EnumDbEngineType
from transactions.rf_db_engine_information import RFDbEngineInformation
from utils.str.rf_utils_str import RFUtilsStr
from beans.field import Field
from transactions.rf_transaction_manager import RFTransactionManager

_dic_db_engines = {}
_dic_information_db_engines = {}
_dic_services = {}
_rf_transaction_manager = None


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
            _dic_information_db_engines[key] = RFDbEngineInformation(key)

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
    def get_fields_table(table_name, db_engine_type):
        """
        Method for get fields for table
        :param table_name: is a name for table to get columns
        :param db_engine_type:
        :return: ar columns if found esle return empty array
        """
        ar_fields = []

        if _dic_information_db_engines is not None and db_engine_type is not None and table_name is not None and \
                db_engine_type in _dic_information_db_engines:
            db_engine_information = _dic_information_db_engines[db_engine_type]

            if table_name in db_engine_information.dic_table_columns:
                ar_fields = db_engine_information.dic_table_columns[table_name]

        return ar_fields

    @staticmethod
    def load_information_db_engine_rf_mysql(database):
        """
        Method for load information db enfine rf_mysql
        :param database: for load information
        :return: None
        """
        rf_mysql_engine = RFContext.get_db_engine(EnumDbEngineType.RF_MYSQL)

        if rf_mysql_engine is not None and RFUtilsStr.is_not_emtpy(database):
            # Load engine information
            rf_db_engine_information = _dic_information_db_engines[EnumDbEngineType.RF_MYSQL]
            dic_table_columns = {}

            connexion = rf_mysql_engine.connect()
            cursor = connexion.cursor()

            # Get columns information per table
            cursor.execute(
                "SELECT COLUMN_NAME , TABLE_NAME FROM `INFORMATION_SCHEMA`.`COLUMNS` "
                " WHERE `TABLE_SCHEMA`=%s ORDER BY TABLE_NAME ASC",
                database)

            records = cursor.fetchall()

            table = None
            ar_records_table = []

            for record in records:

                if table != record[1] and len(ar_records_table):
                    dic_table_columns[table] = ar_records_table
                    ar_records_table = []

                table = record[1]
                ar_records_table.append(Field(name=record[0]))

            if len(ar_records_table):
                dic_table_columns[table] = ar_records_table

            # Close mysql connection
            cursor.close()
            connexion.close()

            rf_db_engine_information.dic_table_columns = dic_table_columns

            # Add db engine information for context
            _dic_information_db_engines[EnumDbEngineType.RF_MYSQL] = rf_db_engine_information

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
