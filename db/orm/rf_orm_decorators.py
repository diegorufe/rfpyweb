from context.rf_context import RFContext
from db.rf_column import RFColumn


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

            # add table for context
            RFContext.add_table(cls)

        return cls

    return decorator_func


def rf_column_decorator(name: str = None, join_property_name: str = None, join_column: str = None,
                        join_table: str = None, join_vo_class_name: str = None,
                        join_table_column: str = 'id'):
    def decorator_func(cls):
        if cls is not None:
            # Add column for table in context
            RFContext.add_column_table(cls.__name__,
                                       RFColumn(name=name, join_property_name=join_property_name,
                                                join_column=join_column,
                                                join_table=join_table, join_vo_class_name=join_vo_class_name,
                                                join_table_column=join_table_column))

        return cls

    return decorator_func
