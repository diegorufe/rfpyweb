from flask import Flask, jsonify
from functools import wraps
from security.enum_secury_auth_mode import EnumSecurityAuthMode
from transactions.rf_transaction_manager import RFTransactionManager
from transactions.enum_db_engine_type import EnumDbEngineType
from transactions.rf_db_engine_information import RFDbEngineInformation

"""

    This class extends Flask for build web applications
    
"""


class RFPyWeb(Flask):

    def __init__(
            self,
            import_name,
            static_url_path=None,
            static_folder="static",
            static_host=None,
            host_matching=False,
            subdomain_matching=False,
            template_folder="templates",
            instance_path=None,
            instance_relative_config=False,
            root_path=None,
            security_check_request_function=None,
            security_auth_mode: EnumSecurityAuthMode = EnumSecurityAuthMode.JWT,
            rf_transaction_manager=None
    ):
        """
        Constructor for web application. This class extends Flask for build lightweight applications
        :param import_name: the name of the application package
        :param static_url_path: can be used to specify a different path for the
                                static files on the web.  Defaults to the name
                                of the `static_folder` folder.
        :param static_folder: The folder with static files that is served at
            ``static_url_path``. Relative to the application ``root_path``
            or an absolute path. Defaults to ``'static'``.
        :param static_host: the host to use when adding the static route.
            Defaults to None. Required when using ``host_matching=True``
            with a ``static_folder`` configured.
        :param host_matching: set ``url_map.host_matching`` attribute.
            Defaults to False.
        :param subdomain_matching: consider the subdomain relative to
            :data:`SERVER_NAME` when matching routes. Defaults to False.
        :param template_folder: the folder that contains the templates that should
                                be used by the application.  Defaults to
                                ``'templates'`` folder in the root path of the
                                application.
        :param instance_path: An alternative instance path for the application.
                              By default the folder ``'instance'`` next to the
                              package or module is assumed to be the instance
                              path.
        :param instance_relative_config: if set to ``True`` relative filenames
                                         for loading the config are assumed to
                                         be relative to the instance path instead
                                         of the application root.
        :param root_path: Flask by default will automatically calculate the path
                          to the root of the application.  In certain situations
                          this cannot be achieved (for instance if the package
                          is a Python 3 namespace package) and needs to be
                          manually defined.
        :param security_check_request_function: function for execute extra check validation request function. First
        argument is rf_py_web application, second argument is path for request, third argument is the request
        :param security_auth_mode: Mode for login and secure path request. For default value is JWT
        :param rf_transaction_manager for manage transaction. See configure_transaction_manager for this class
        """
        # Call super constructor from Flask
        Flask.__init__(
            self, import_name, static_url_path=static_url_path, static_folder=static_folder, static_host=static_host,
            host_matching=host_matching, subdomain_matching=subdomain_matching, template_folder=template_folder,
            instance_path=instance_path, instance_relative_config=instance_relative_config, root_path=root_path
        )
        # Function for check security
        self.security_check_request_function = security_check_request_function
        # Mode security
        # if is none default jwt
        self.security_auth_mode = security_auth_mode if not None else EnumSecurityAuthMode.JWT
        self.rf_transaction_manager = rf_transaction_manager
        self.dic_db_engines = {}
        self.dic_information_db_engines = {}
        self.dic_services = {}

    def json(self, *args, **kwargs):
        """
        Method for convert data to json.
        :return: data convert to json
        """
        return jsonify(*args, **kwargs)

    def configure_transaction_manager(self, function_create_transaction=None, function_commit_transaction=None,
                                      function_rollback_transaction=None):
        """
        Method  for configure transaction manager
        :param function_create_transaction: this function must be params enum_transaction_type and params=None
        :param function_commit_transaction: this function must be params rf_transaction and params=None
        :param function_rollback_transaction: this function must be params rf_transaction and params=None
        :return: None
        """
        self.rf_transaction_manager = RFTransactionManager(function_create_transaction=function_create_transaction,
                                                           function_commit_transaction=function_commit_transaction,
                                                           function_rollback_transaction=function_rollback_transaction)

    def __check_secure_request__(self, path_request):
        """
        Method for check secure request
        :param path_request: to check
        :return: response for request path request
        """
        print("Route: " + path_request)
        response_check_secure = None

        # first check toke if security is jwt
        if self.security_auth_mode == EnumSecurityAuthMode.JWT:
            # TODO check token jwt
            pass

        # If has security check function call this for check secure request
        if self.security_check_request_function is not None:
            response_check_secure = self.security_check_request_function(self, path_request, None)

        return response_check_secure

    def secure_filter_decorator(self, path_request: str):
        """
        Method for request secure filers
        :param path_request: for check secure filter
        :return: function execute secure filter
        """

        def decorator(f):
            @wraps(f)
            def wrapper(*args, **kwargs):

                # check security request
                response_check_secure = self.__check_secure_request__(path_request)

                if response_check_secure is None:
                    return f(*args, **kwargs)
                else:
                    return response_check_secure

            return wrapper

        return decorator

    def add_db_engine(self, key: EnumDbEngineType, db_engine):
        """
        Method for add db engine. This method only add db_engine if not None and key not None
        :param key: for db engine
        :param db_engine: to add
        :return: None
        """
        if key is not None and db_engine is not None:
            self.dic_db_engines[key] = db_engine
            self.dic_information_db_engines[key] = RFDbEngineInformation(key)

    def get_db_engine(self, key: EnumDbEngineType):
        """
        Method for get db engine by key. If key is None or dont find engine return None
        :param key: for get db engine
        :return: db engine if found else return None
        """
        db_engine = None
        if key is not None and key in self.dic_db_engines:
            db_engine = self.dic_db_engines[key]
        return db_engine

    def create_db_engine_rf_mysql(self, database: str, user: str, password: str):
        """
        Method for create engine rf mysql
        :param database: for connect to database
        :param user: for connect to database
        :param password: for connect to database
        :return: None
        """
        from flaskext.mysql import MySQL
        from beans.field import Field
        self.config['MYSQL_DATABASE_USER'] = user
        self.config['MYSQL_DATABASE_PASSWORD'] = password
        self.config['MYSQL_DATABASE_DB'] = database
        mysql = MySQL()
        mysql.init_app(self)
        self.add_db_engine(EnumDbEngineType.RF_MYSQL, mysql)

        # Load engine information
        rf_db_engine_information = self.dic_information_db_engines[EnumDbEngineType.RF_MYSQL]
        dic_table_columns = {}

        connexion = mysql.connect()
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

        # Add db engine information for transaction
        self.rf_transaction_manager.dic_information_db_engines[EnumDbEngineType.RF_MYSQL] = rf_db_engine_information

    def add_service(self, key, service):
        """
        Method for add service. Only add if key is not none and service is not none and key dont find in service
        :param key: to add service
        :param service: to add
        :return: None
        """
        if key is not None and service is not None and key not in self.dic_services:
            self.dic_services[key] = service

    def get_service(self, key):
        """
        Method for get service
        :param key: for get service
        :return: service if found by key else return None
        """
        service = None
        if key is not None and key in self.dic_services:
            service = self.dic_services[key]
        return service