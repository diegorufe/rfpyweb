import enum


class EnumDbEngineType(enum.Enum):
    """
    Enum for db engine types
    """
    RF_MYSQL = "rf_mysql"
    RF_MYSQL_POOL = "rf_mysql_pool"
