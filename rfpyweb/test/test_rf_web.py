from rfpyweb.core.rf_py_web import RFPyWeb
from rfpyweb.test.test_route import TestForeRoute
from rfpyweb.test.test_dao import TestDao, TestForeDao
from rfpyweb.test.test_bo import TestBo, TestForeBo

rf_py_web = RFPyWeb(__name__)

# Create rf_mysql engine
rf_py_web.create_db_engine_rf_mysql('test', 'root', 'root')

# Add services
rf_py_web.add_service('testbo', TestBo(TestDao()))

rf_py_web.add_service('testforebo', TestForeBo(TestForeDao()))

# Examples of routes
TestForeRoute(rf_py_web=rf_py_web).load()

rf_py_web.run(debug=True)
