class Field:

    def __init__(self, name=None, alias_table=None, alias_field=None, custom_field=None):
        """
        Constructor for class field
        :param name: is the name for field
        :param alias_table: for get the field
        :param alias_field: for field
        :pmara custom_field: for field ignore name, alias ...
        """
        self.name = name
        self.alias_table = alias_table
        self.alias_field = alias_field
        self.custom_field = custom_field
