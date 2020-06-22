from routes.crud.rf_base_crud_route import RFBaseCrudRoute
from decimal import Decimal


class TestForeRoute(RFBaseCrudRoute):

    def __init__(self, rf_py_web=None):
        RFBaseCrudRoute.__init__(self, rf_py_web=rf_py_web, path_requests='/test', service_name='testforebo')

    def list(self):
        response = None
        response_bo = None
        if self.service is not None:
            from beans.query.filter import Filter
            from beans.query.join import Join
            from constants.query.enum_filter_type import EnumFilterType
            from constants.query.enum_join_type import EnumJoinType
            from beans.query.order import Order

            ar_filters = [Filter(field='testVoBis.code', value='03', filter_type=EnumFilterType.EQUAL)]
            ar_joins = [Join(field="testVo", join_type=EnumJoinType.INNER_JOIN_FETCH),
                        Join(field="testVoBis", join_type=EnumJoinType.INNER_JOIN_FETCH)]
            ar_orders = [Order(field="testVoBis.code")]
            # ar_joins = []
            # count = self.service.count(ar_filters=ar_filters, ar_joins=ar_joins)
            response_bo = self.service.list(ar_filters=ar_filters, ar_joins=ar_joins, ar_orders=ar_orders)

        if response_bo is not None:
            response = self.rf_py_web.json(response_bo)

        return response

    def add(self):
        from test.test_vo import TestVo
        vo = self.service.new_instance_vo()

        vo.descr = 'asd'
        vo.amount = Decimal("14.453")
        vo.testVo = TestVo()
        vo.testVo.id = 2

        self.service.add(vo)

        return self.rf_py_web.json(vo)

    def edit(self):
        from test.test_vo import TestVo
        ar_pks_values = [7]
        vo = self.service.read(ar_pks_values)
        vo.id = 6

        vo.descr = 'asd'
        vo.amount = Decimal("20.453")
        vo.testVo = TestVo()
        vo.testVo.id = 1

        self.service.edit(vo)

        return self.rf_py_web.json(vo)

    def delete(self):
        from test.test_vo import TestVo
        ar_pks_values = [7]
        result = self.service.delete(ar_pks_values)

        return self.rf_py_web.jsonify(deleted=result)
