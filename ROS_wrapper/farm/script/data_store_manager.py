from log import Log
from rule import Rule

class DataStoreManager(object):

    dac_threads = dict()

    def __init__(self):
        pass

    def append_dac_thread(self, did, dac_thread):
        DataStoreManager.dac_threads[did] = dac_thread

    def get_dac_thread_by_id(self, did):
        return DataStoreManager.dac_threads[did]

    def assign_end_device_to_dac(self, did, end_device):
        if end_device.is_sensor:
            for dac_thread in DataStoreManager.dac_threads.values():
                dac_thread.assign_end_device(end_device)
        else:
            dac_thread = self.get_dac_thread_by_id(did)
            dac_thread.assign_end_device(end_device)

    @staticmethod
    def assign_schedule_to_dac(rpc_schedule):
        rules = list()
        for rule in rpc_schedule:
            r = Rule()
            if not r.initialize(rule):
                return False
            rules.append(r)
        for rule in rules:
            action_in_same_dac = set(rule.target_did)
            for action in rule.actions:
                target = action['actuator']
                if target['DID'] in action_in_same_dac:
                    thread = DataStoreManager.dac_threads[target['DID']]
                    thread.assign_rule_to_dac_schedule(rule)
                    action_in_same_dac.remove(target['DID'])
        return True

    @staticmethod
    def get_sensor_value_by_tid(tid):
        sensor_seq = DataStoreManager.dac_threads[0].sensor_seq
        for sensor in sensor_seq.values():
            if sensor.TID == tid:
                return sensor.get_value()
        return 'FAILURE'
