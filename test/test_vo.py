from vo.rf_base_vo import RFBaseVo


class TestVo(RFBaseVo):

    def __init__(self):
        RFBaseVo.__init__(self, table_name='test')
        self.id = None
        self.code = None


class TestForeVo(RFBaseVo):

    def __init__(self):
        RFBaseVo.__init__(self, table_name='testfore')
        self.id = None
        self.descr = None
        self.testId = None
