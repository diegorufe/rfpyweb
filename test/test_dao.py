from dao.rf_base_dao import RFBaseDao
from test.test_vo import TestVo
from transactions.enum_db_engine_type import EnumDbEngineType


class TestDao(RFBaseDao):

    def __init__(self):
        RFBaseDao.__init__(self, vo_class=TestVo, db_engine_type=EnumDbEngineType.RF_MYSQL)
