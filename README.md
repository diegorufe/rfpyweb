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


