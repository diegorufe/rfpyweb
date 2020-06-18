def rf_table_decorator(table_name: str = None, pk_field: str = 'id'):
    """
    Decorator for ser the table for class
    :param table_name: for class
    :param pk_field: for class
    :return: class to decorate
    """

    def decorator_func(cls):
        if cls is not None:
            # Set table name for class
            if cls.__table_name__ is None:
                cls.__table_name__ = table_name
            # Set pk for field
            if cls.__pk_field__ is None:
                cls.__pk_field__ = pk_field

        return cls

    return decorator_func
