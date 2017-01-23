from log import Log
import threading
import Queue
import time

log = Log(Log.DEBUG, __file__)

def subscribe_every_sensor():
    while True:
        for sensor in DACController.sensor_seq.values():
            sensor.subscribe_value()
        time.sleep(0.1)
def run_subscribe():
    threading.Thread(target=subscribe_every_sensor).start()

class DACController(threading.Thread):

    sensor_seq = dict()

    def __init__(self, data_store_manager, cid, did):
        threading.Thread.__init__(self)
        # arguments
        self.cid = cid
        self.did = did
        self.data_store_manager = data_store_manager
        self.schedule_queue = Queue.Queue()
        self.actuator_seq = dict()
        self.actuator_immediate = dict()

    def initial(self):
        # initial
        self.data_store_manager.append_dac_thread(self.did, self)
        # start thread
        self.start()


    def get_end_device_from_id(self, end_device_id):
        if end_device_id['TYPE'][0] == 'S':
            temp_device_seq = DACController.sensor_seq
        elif end_device_id['TYPE'][0] == 'A':
            temp_device_seq = self.actuator_seq

        for device in temp_device_seq.values():
            if (end_device_id['CID'] == device.CID and
                end_device_id['DID'] == device.DID and
                end_device_id['TYPE'] == device.TYPE and
                end_device_id['TID'] == device.TID and
                end_device_id['ADDRESS'] == device.ADDRESS):
                    return device
        return False

    def assign_end_device(self, end_device):
        if end_device.is_actuator:
            self.actuator_seq[end_device.TID] = end_device
            log.info('DAC {0} append an actuator, type {1}, tid {2}'.format(self.did, end_device.TYPE, end_device.TID))
        elif end_device.is_sensor:
            DACController.sensor_seq[end_device.TID] = end_device
            log.info('DAC {0} append a sensor, type {1}, tid {2}'.format(self.did, end_device.TYPE, end_device.TID))
        else:
            log.error('wrong device tyep')

    def assign_rule_to_dac_schedule(self, rule):
        self.schedule_queue.put(rule)
        #self.actuator_immediate[rule.target_tid] = False

    def run(self):

        while True:
            # get a device from schedule queue
            # if queue is empyt than block
            rule = self.schedule_queue.get()

            for sensor in DACController.sensor_seq.values():
                print(sensor.TYPE, sensor.get_value())

            if rule.immediate_control:
                for action in rule.actions:
                    target = action['actuator']
                    target_actuator = self.get_end_device_from_id(target)
                    if target_actuator:
                        target_actuator.make_action(action['value'])


            elif rule.duration_control:
                if rule.get_start_time_delta() < 0:
                    for action in rule.actions:
                        target = action['actuator']
                        target_actuator = self.get_end_device_from_id(target)
                    if target_actuator:
                        target_actuator.schedule_action(action['value'], rule.duration)
                else:
                    self.schedule_queue.put(rule)
'''
            elif rule.condition_control:
                and_condition = True
                for i in range(len(rule.conditions)):
                    reference_sensor = rule.reference_sensors[i]
                    operator = rule.sensor_operators[i]
                    threshold = rule.operator_thresholds[i]
                    sensor = self.get_end_device_from_id(reference_sensor)
                    if sensor == False:
                        and_condition = False
                        break
                    sensor_value = sensor.get_value()
                    if not rule.check_condition(sensor_value, operator, threshold):
                        and_condition = False
                        break

                if and_condition:
                    target_actuator = self.actuator_seq[rule.target_tid]
                    target_actuator.make_action(rule.action)
                
                self.schedule_queue.put(rule)
                time.sleep(0.1)
'''
