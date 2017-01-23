from end_device import EndDevice
import rospy
from std_msgs.msg import String, Float32, Int16
import sys
sys.path.append('../src')

class Sensor(EndDevice):
    def __init__(self, cid, did, Type, tid, address, topic, msg):
        super(Sensor, self).__init__(cid, did, Type, tid, address)
        self.topic = topic
        self.msg = msg
        self.value = 0

    def callback(self, data):
        if self.TYPE == 'ST':
            self.value = data.airtemperature
        elif self.TYPE == 'SH':
            self.value = data.airhumidity
        elif self.TYPE == 'SHE':
            self.value = data.soilhumidity
        elif self.TYPE == 'SPH':
            self.value = data.ph
        elif self.TYPE == 'SI':
            self.value = data.ir

    def subscribe_value(self):
        #if self.TYPE == 'SI':
        rospy.Subscriber(self.topic, self.msg, self.callback)

    def get_value(self):
        return self.value
