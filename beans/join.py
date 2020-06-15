from constants.enum_join_type import EnumJoinType


class Join:

    def __init__(self, join_table=None, join_alias=None, join_condition=None,
                 join_type: EnumJoinType = EnumJoinType.INNER_JOIN):
        """
        Constructor for class join
        :param join_table: join table
        :param join_alias: for join
        :param join_condition: for join
        :param join_type: for join
        """
        self.join_table = join_table
        self.join_alias = join_alias
        self.join_condition = join_condition
        self.join_type = join_type
