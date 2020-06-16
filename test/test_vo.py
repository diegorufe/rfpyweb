from vo.rf_base_vo import RFBaseVo


class TestVo(RFBaseVo):

    def __init__(self):
        RFBaseVo.__init__(self, 'test')
        self.id = None
        self.code = None
