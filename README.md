# rfpyweb

Web library for flask in python

Experimental history for library, in process ....

## Beans

### field.py 

> Field:  Class to store value for field store data
>
>- Methods:
>
    def __init__(self, join_table: str = None, join_alias: str = None, join_field: str = None,
                 join_type: EnumJoinType = EnumJoinType.INNER_JOIN, custom_query_join: str = None,
                 join_table_field: str = "id"):
        """
        Constructor for class join
        :param join_table: join table
        :param join_alias: for join
        :param join_field: for join
        :param join_type: for join
        :param custom_query_join if is not None use this for join data
        :param join_table_field: is field for join in join table
        """
> Limit: Class to limit result for find data
> - Methods:
>
    def __init__(self, start: int = 0, end: int = 0):
        """
        Constructor for limit
        :param start: for query
        :param end: of query
        """

### join.py

> Join: Class to join store data
>
> - Methods:
>
    def __init__(self, join_table=None, join_alias=None, join_field=None,
                 join_type: EnumJoinType = EnumJoinType.INNER_JOIN, custom_query_join=None):
        """
        Constructor for class join
        :param join_table: join table
        :param join_alias: for join
        :param join_field: for join
        :param join_type: for join
        :param custom_query_join if is not None use this for join data
        """

## BO

### rf_base_bo.py

> RFBaseBo: Class for call business logic
>- Methods:
>    
     def __init__(self, dao=None, transaction_manager: RFTransactionManager = None):
        """
        Constructor for base bo
        :param dao: dao for bo,. Can be None
        :param transaction_manager: for manage transactions. Can be None
        """
 
## Context

### rf_context.py

> RFContext: Class contains context methods
>- Methods:
>
    @staticmethod
    def add_service(key, service):
        """
        Method for add service. Only add if key is not none and service is not none and key dont find in service
        :param key: to add service
        :param service: to add
        :return: None
        """  
>
    @staticmethod
    def get_service(key):
        """
        Method for get service
        :param key: for get service
        :return: service if found by key else return None
        """
>
    @staticmethod
    def add_db_engine(key: EnumDbEngineType, db_engine):
        """
        Method for add db engine. This method only add db_engine if not None and key not None
        :param key: for db engine
        :param db_engine: to add
        :return: None
        """
>
    @staticmethod
    def get_db_engine(key: EnumDbEngineType):
        """
        Method for get db engine by key. If key is None or dont find engine return None
        :param key: for get db engine
        :return: db engine if found else return None
        """
>
    @staticmethod
    def get_fields_table(table_name, db_engine_type):
        """
        Method for get fields for table
        :param table_name: is a name for table to get columns
        :param db_engine_type:
        :return: ar columns if found esle return empty array
        """
>
    @staticmethod
    def load_information_db_engine_rf_mysql(database):
        """
        Method for load information db enfine rf_mysql
        :param database: for load information
        :return: None
        """   
>
    @staticmethod
    def get_transaction_manager():
        """
        Method for get transaction manager
        :return: transaction manager 
        """   
        
## Utils

### array 

#### rf_utils_array.py

> RFUtilsArray: class for utilities for arrays 
>- Methods:
>
    @staticmethod
    def is_not_empty(array):
        """
        Method to check array is not empty.
        :param array: to check
        :return: True if array is not None isinstance (list, tuple) and len > 0
        """
>
    @staticmethod
    def is_empty(array):
        """
        Method to check array is empty
        :param array: to check
        :return: True if is None not instance (list, tuple) or len = 0
        """

### built

#### rf_utils_built.py

> RFUtilsBuilt: class for utilities built
>- Methods:
>
    @staticmethod
    def has_attr(object_attr, attr):
        """
        Method to know has attr
        :param object_attr: to check if has attr
        :param attr: to check
        :return: True if object_attr is not None and not empty attr and hasattr
        """
>
    @staticmethod
    def get_attr(object_attr, attr):
        """
        Method for get attr for object
        :param object_attr: to get attr
        :param attr: to get
        :return: attr if find else return None
        """
>
    @staticmethod
    def set_attr(object_attr, attr, value_to_set):
        """
        Method for set attr
        :param object_attr: to set attr
        :param attr: to set value
        :param value_to_set:
        :return: True if set attr False if not
        """
        
### str

#### rf_utils_str.py

> RFUtilsStr: class for utilities built
>- Methods:
>
    @staticmethod
    def is_not_emtpy(value):
        """
        Method to check value is not empty
        :param value: to check
        :return: True if value is not None and isinstance str and strip() != ""
        """
>
    @staticmethod
    def is_empty(value):
        """
        Method to check value is empty
        :param value: to check
        :return: True if value is None or non instance of str or value.strip() == ""
        """
>

    @staticmethod
    def split(value, separator):
        """
        Method for split str
        :param value: to split
        :param separator: for apply split
        :return: data split if value is not empty and separator is not None
        """
>
    @staticmethod
    def unique_str(time_execute: int = 1):
        """
        Method for generate unique str
        :param time_execute for exeucte concat unique str
        :return: unique str
        """


