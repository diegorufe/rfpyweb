# rfpyweb

Web library for flask in python

Experimental history for library, in process ....

## Beans

### field.py 

> Field:  Class to store value for field store data
>
>- Methods:
>
    def __init__(self, name=None, alias_table=None, alias_field=None):
        """
        Constructor for class field
        :param name: is the name for field
        :param alias_table: for get the field
        :param alias_field: for field
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
## Utils

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


