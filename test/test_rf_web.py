from core.rf_py_web import RFPyWeb
from routes.crud.rf_base_crud_route import RFBaseCrudRoute
from test.test_dao import TestDao
from test.test_bo import TestBo

rf_py_web = RFPyWeb(__name__)

# Create rf_mysql engine
rf_py_web.create_db_engine_rf_mysql('test', 'root', 'root')

# Add services
rf_py_web.add_service('test_bo', TestBo(TestDao()))

# Examples of routes
RFBaseCrudRoute(rf_py_web=rf_py_web, path_requests='/test', service_name='test_bo').load()

rf_py_web.run(debug=True)
