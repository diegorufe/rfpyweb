from core.rf_py_web import RFPyWeb
from routes.crud.rf_base_crud_route import RFBaseCrudRoute
from routes.rf_base_route import RFBaseRoute

rf_py_web = RFPyWeb(__name__)

# Create rf_mysql engine
rf_py_web.create_db_engine_rf_mysql('test', 'root',  'root')

# Example for transaction
rf_py_web.configure_transaction_manager()

# Examples of routes
RFBaseRoute(rf_py_web=rf_py_web, path_requests='/test').load()
RFBaseCrudRoute(rf_py_web=rf_py_web, path_requests='/clients').load()

rf_py_web.run(debug=True)
