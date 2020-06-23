import enum


class EnumSecurityAuthMode(enum.Enum):
    """
    Enum for security auth modes
    """
    JWT = "JWT"
    BASIC = "BASIC"
