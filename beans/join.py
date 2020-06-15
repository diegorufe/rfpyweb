from constants.enum_join_type import EnumJoinType


class Join:

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
        self.join_table = join_table
        self.join_alias = join_alias
        self.join_field = join_field
        self.join_type = join_type
        self.custom_query_join = custom_query_join
