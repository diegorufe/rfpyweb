"""

    Module for class base vo

"""


class RFBaseVo:

    def __init__(self, table_name: str):
        """
        Class vo for dao
        :param table_name: for database
        """
        self.table_name = table_name

    def to_dto(self):
        """
        Method for convert data inside this to DTO
        :return: DTO object data inside this
        """
        pass

    def wrap(self, dto):
        """
        Method for wrap data dto to this
        :param dto: for wrap data
        :return: None
        """
        pass
