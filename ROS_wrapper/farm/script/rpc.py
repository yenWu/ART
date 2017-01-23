from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler
from data_store_manager import DataStoreManager
import threading
import xmlrpclib

ip = 'http://192.168.1.30:8000'

###############################################################
# rpc client for server

def rpc_register(device, _id):
    s = xmlrpclib.ServerProxy(ip)
    print(s.register(device, _id))

def rpc_event(device, _id):
    s = xmlrpclib.ServerProxy(ip)
    print(s.event('disconnect', device, _id))

###############################################################
# rpc server for server

class ReuqestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

def rpc_set_rule(rpc_schedule):
    if DataStoreManager.assign_schedule_to_dac(rpc_schedule):
        return 'SUCCESS'
    else:
        return 'FAILURE'

def rpc_set_imm_rule(rpc_rule):
    if DataStoreManager.assign_schedule_to_dac(rpc_rule):
        return 'SUCCESS'
    else:
        return 'FAILURE'

def rpc_get_sensor_value(tid):
    print('get_', tid)
    return DataStoreManager.get_sensor_value_by_tid(tid)

def rpc_server(cid):
    server = SimpleXMLRPCServer((cid, 8000),
                                requestHandler=ReuqestHandler,
                                allow_none=True)
    server.register_introspection_functions()

    server.register_function(rpc_set_rule, 'rpc_set_rule')

    server.register_function(rpc_set_imm_rule, 'rpc_set_imm_rule')

    server.register_function(rpc_get_sensor_value, 'rpc_get_sensor_value')

    server.serve_forever()

def run_rpc_server(cid):
    threading.Thread(target=rpc_server, args=(cid,)).start()

#####################################################################
