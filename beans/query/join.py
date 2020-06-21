from constants.query.enum_join_type import EnumJoinType


class Join:

    def __init__(self, field: str = None, join_type: EnumJoinType = EnumJoinType.INNER_JOIN,
                 alias: str = None, custom_query_join: str = None):
        """
        Constructor for class join
        :param field: for join
        :param join_type: for join
        :param alias alias jor join
        :param custom_query_join if is not None use this for join data
        """
        self.field = field
        self.join_type = join_type
        self.alias = alias
        self.custom_query_join = custom_query_join
