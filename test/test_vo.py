from vo.rf_base_vo import RFBaseVo
from db.orm.rf_orm_decorators import rf_table_decorator, rf_column_decorator


@rf_column_decorator(name='id')
@rf_column_decorator(name='code')
@rf_table_decorator(table_name='test')
class TestVo(RFBaseVo):

    def __init__(self):
        RFBaseVo.__init__(self)
        self.id = None
        self.code = None


@rf_column_decorator(name='id')
@rf_column_decorator(name='descr')
@rf_column_decorator(name='testVo', column_name="testId", join_table="test", join_vo_class_name="TestVo")
@rf_column_decorator(name='testVoBis', column_name="testIdBis", join_table="test", join_vo_class_name="TestVo")
@rf_table_decorator(table_name='testfore')
class TestForeVo(RFBaseVo):

    def __init__(self):
        RFBaseVo.__init__(self)
        self.id = None
        self.descr = None
        self.testVo = None
        self.testVoBis = None
