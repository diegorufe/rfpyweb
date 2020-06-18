from db.orm.rf_orm_decorators import rf_table_decorator
from vo.rf_base_vo import RFBaseVo


@rf_table_decorator(table_name='test')
class TestVo(RFBaseVo):

    def __init__(self):
        RFBaseVo.__init__()


print(TestVo.__table_name__)
delattr(TestVo, '__table_name__')
print(TestVo.__table_name__)
