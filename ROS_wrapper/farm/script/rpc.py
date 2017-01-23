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

def rpc_set_rule(rpc_schedule):
    print(rpc_schedule)
    if DataStoreManager.assign_schedule_to_dac(rpc_schedule):
        return 'SUCCESS'
    else:
        return 'FAILURE'

def rpc_set_imm_rule(rpc_rule):
    print(rpc_rule)
    if DataStoreManager.assign_schedule_to_dac(rpc_rule):
        return 'SUCCESS'
    else:
        return 'FAILURE'

def rpc_get_sensor_value(tid):
    print('get_', tid)
    return DataStoreManager.get_sensor_value_by_tid(tid)

def rpc_ios_rule(schedule):
    schedule['condition'] = None
    action = schedule['action']
    actuator = action['actuator']
    a=actuator['ADDRESS']
    actuator['ADDRESS'] = int(a)
    value = action['value']
    temp = {'actuator':actuator, 'value':value}
    schedule['action'] = [temp]
    schedule['period'] = {'start_time':'22', 'duration':0}
    schedule['rule_make_time'] = '2017-00-00 00:00:00'
    schedule = [schedule]
    if DataStoreManager.assign_schedule_to_dac(schedule):
        return 'SUCCESS'
    else:
        return 'FAILURE'

def rpc_server(cid):
    server = SimpleXMLRPCServer((cid, 8000),
                                allow_none=True)
    server.register_introspection_functions()

    server.register_function(rpc_set_rule, 'rpc_set_rule')

    server.register_function(rpc_set_imm_rule, 'rpc_set_imm_rule')

    server.register_function(rpc_get_sensor_value, 'rpc_get_sensor_value')

    server.register_function(rpc_ios_rule, 'rpc_ios_rule')

    server.serve_forever()

def run_rpc_server(cid):
    threading.Thread(target=rpc_server, args=(cid,)).start()

#####################################################################
