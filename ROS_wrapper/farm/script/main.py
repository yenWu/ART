from log import Log
from data_store_manager import DataStoreManager
from DAC_controller import DACController, run_subscribe
from rpc import run_rpc_server, rpc_register
from actuator import Actuator
from sensor import Sensor
import os
import rospy
from std_msgs.msg import String, Int16
import sys
sys.path.append('../src')
from farm.msg import sunlight, air_meter, ph_meter, soil_meter, sprinkler

def initlize_ros():
    pub1 = rospy.Publisher('/sprinkler', sprinkler, queue_size=10)
    pub2 = pub1
    pub4 = pub1
    sub0 = '/airmeter'
    sub1 = '/airmeter'
    sub2 = '/phmeter'
    sub3 = '/soilmeter'
    sub4 = '/sunlight'
    rospy.init_node('controller', anonymous=True)
    rate = rospy.Rate(10)
    return pub1, pub2, pub4, sub0, sub1, sub2, sub3, sub4

def main():

    log = Log(Log.DEBUG, __file__)

    cid = get_controller_ip()
    log.info('controller ip: {0}'.format(cid))

    data_store_manager = DataStoreManager()

    log.info('start rpc server')
    run_rpc_server(cid)

    pub1, pub2, pub4, sub0, sub1, sub2, sub3, sub4 = initlize_ros()

    print('start')

##########################################################################
# dac 0
    did = 0
    log.info('start a new dac thread, did: {0}'.format(did))
    thread = DACController(data_store_manager, cid, did)
    thread.initial()

    tid = 0
    log.info('new temp sensor at did: {0}, type:{1}, tid:{2}'.format(did, 'S', tid))
    temp = Sensor(cid, did, 'ST', tid, 40000, sub0, air_meter)
    data_store_manager.assign_end_device_to_dac(did, temp)

    tid = 1
    log.info('new humid sensor at did: {0}, type:{1}, tid:{2}'.format(did, 'SH', tid))
    humid = Sensor(cid, did, 'SH', tid, 40001, sub1, air_meter)
    data_store_manager.assign_end_device_to_dac(did, humid)

    tid = 2
    log.info('new soil temp sensor at did: {0}, type:{1}, tid:{2}'.format(did, 'SHE', tid))
    soil_temp = Sensor(cid, did, 'SHE', tid, 40002, sub2, soil_meter)
    data_store_manager.assign_end_device_to_dac(did, soil_temp)

    tid = 3
    log.info('new ph sensor at did: {0}, type:{1}, tid:{2}'.format(did, 'SPH', tid))
    soil_ph = Sensor(cid, did, 'SPH', tid, 40003, sub3, ph_meter)
    data_store_manager.assign_end_device_to_dac(did, soil_ph)

    tid = 4
    log.info('new light sensor at did: {0}, type:{1}, tid:{2}'.format(did, 'SI', tid))
    light = Sensor(cid, did, 'SI', tid, 40004, sub4, sunlight)
    data_store_manager.assign_end_device_to_dac(did, light)

########################################################################
# dac 1
    did = 1
    log.info('start a new dac thread, did: {0}'.format(did))
    thread = DACController(data_store_manager, cid, did)
    thread.initial()

    tid = 5
    log.info('new irrigrate actuator at did: {0}, type:{1}, tid:{2}'.format(did, 'AW', tid))
    irr = Actuator(cid, did, 'AW', tid, 40005, pub1, sprinkler)
    data_store_manager.assign_end_device_to_dac(did, irr)

    tid = 6
    log.info('new irrigrate actuator at did: {0}, type:{1}, tid:{2}'.format(did, 'AW', tid))
    irr = Actuator(cid, did, 'AW', tid, 40006, pub2, sprinkler)
    data_store_manager.assign_end_device_to_dac(did, irr)

    tid = 7
    log.info('new irrigrate actuator at did: {0}, type:{1}, tid:{2}'.format(did, 'AW', tid))
    irr = Actuator(cid, did, 'AW', tid, 40007, pub4, sprinkler)
    data_store_manager.assign_end_device_to_dac(did, irr)

########################################################################
# register device
    '''
    rpc_register('controller', {'CID':cid})
    rpc_register('dac', {'CID':cid, 'DID':'0'})
    rpc_register('sensor', {'CID':cid, 'DID':'0', 'Type':'ST', 'TID':'0', 'Address': '40000'})
    rpc_register('sensor', {'CID':cid, 'DID':'0', 'Type':'SH', 'TID':'1', 'Address': '40001'})
    rpc_register('sensor', {'CID':cid, 'DID':'0', 'Type':'SHT', 'TID':'2', 'Address': '40002'})
    rpc_register('sensor', {'CID':cid, 'DID':'0', 'Type':'SPH', 'TID':'3', 'Address': '40003'})
    rpc_register('sensor', {'CID':cid, 'DID':'0', 'Type':'SI', 'TID':'4', 'Address': '40004'})
    rpc_register('dac', {'CID':cid, 'DID':'1'})
    rpc_register('actuator', {'CID':cid, 'DID':'1', 'Type':'AW', 'TID':'5', 'Address': '40005'})
    rpc_register('actuator', {'CID':cid, 'DID':'1', 'Type':'AW', 'TID':'6', 'Address': '40006'})
    rpc_register('actuator', {'CID':cid, 'DID':'1', 'Type':'AW', 'TID':'7', 'Address': '40007'})
    '''
########################################################################
    run_subscribe()

def get_controller_ip():
    f = os.popen('ifconfig | grep "inet\ addr" | grep -v "127.0.0.1" | cut -d: -f 2 | cut -d" " -f 1 | tr -d "\n"')
    ip = f.read()
    if ip == '':
        ip = '127.0.0.1'
    return ip

if __name__ == "__main__":
    main()
