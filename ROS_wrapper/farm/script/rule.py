from log import Log
import datetime

log = Log(Log.DEBUG, __file__)

class Rule(object):

    ''' a sample rule
    {
        'condition':['if sensor1 > 40%'],
        'action':{ {CID, DID...}, 1 for open else 0 for close]
        'period':{ 'start_time': time.., 'duration': #seconds}
        'rule_make_time':time..
    }
    '''

    def __init__(self):
        self.immediate_control = False
        self.duration_control = False
        self.condition_control = False
        self.condition_control_with_duration = False

        self.reference_sensors = list()
        self.sensor_operators = list()
        self.operator_thresholds = list()

        self.target_cid = list()
        self.target_did = list()
        self.target_Type = list()
        self.target_tid = list()
        self.target_address = list()
        self.target_value = list()

    def initialize(self, rule):
        try:
            self.conditions = rule['condition']
            if self.conditions != None:
                for condition in self.conditions:
                    self.reference_sensors.append(condition['sensor'])
                    self.sensor_operators.append(condition['operator'])
                    self.operator_thresholds.append(condition['threshold'])
            # target actuator action
            self.actions = rule['action']
            for action in self.actions:
                target = action['actuator']
                self.target_cid.append(target['CID'])
                self.target_did.append(target['DID'])
                self.target_Type.append(target['TYPE'])
                self.target_tid.append(target['TID'])
                self.target_address.append(target['ADDRESS'])
                value = action['value']
                self.target_value.append(value)
            # start time and duration
            self.period = rule['period']
            self.start_time = self.period['start_time']
            self.duration = self.period['duration']
            # the time where this rule make
            self.rule_make_time = rule['rule_make_time']
            # initial
        except KeyError:
            return False

        if not self.conditions and self.duration == 0:
            self.immediate_control = True

        if not self.conditions and self.duration != 0:
            self.duration_control = True

        if self.conditions and self.duration == 0:
            self.condition_control = True

        if self.conditions and self.duration != 0:
            self.condition_control_with_duration = True

        return True

    def get_start_time_delta(self):
        now = datetime.datetime.now()
        start_time = datetime.datetime.strptime(self.start_time, '%Y-%m-%d %H:%M:%S')
        delta = (start_time - now).total_seconds()
        return delta

    def check_condition(self, value, operator, threshold):
        if operator == 1:
            return True if value > threshold else False

        return False
