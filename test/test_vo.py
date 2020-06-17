from vo.rf_base_vo import RFBaseVo


class TestVo(RFBaseVo):

    def __init__(self):
        RFBaseVo.__init__(self, table_name='test')
        self.id = None
        self.code = None
