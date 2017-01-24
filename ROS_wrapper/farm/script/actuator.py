from end_device import EndDevice
from threading import Timer
import time

class Actuator(EndDevice):

    r1 = 0
    r2 = 0
    r3 = 0

    def __init__(self, cid, did, Type, tid, address, pub, sprinkler):
        super(Actuator, self).__init__(cid, did, Type, tid, address)
        self.curr_setting = 0
        self.publisher = pub
        self.sprinkler = sprinkler

    def make_action(self, action):
        if self.TID == 6:
            Actuator.r1 = action
        if self.TID == 7:
            Actuator.r2 = action
        if self.TID == 8:
            Actuator.r3 = action
        self.publisher.publish(relay1=Actuator.r1, relay2=Actuator.r2, relay3=Actuator.r3)
        print('actuator {0} take an action {1}'.format(self.TID, action))
        print(Actuator.r1, Actuator.r2, Actuator.r3)
        self.curr_setting = action

    def schedule_action(self, action, duration):
        pre_action = self.curr_setting
        self.make_action(action)
        self.timer = Timer(duration, self.make_action, (pre_action,)).start()

    def stop_schedule_action(self):
        if self.timer:
            self.timer.cancel()
