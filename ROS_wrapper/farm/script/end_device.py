class EndDevice(object):
    def __init__(self, cid, did, Type, tid, address):
        self.CID = cid
        self.DID = did
        self.TYPE = Type
        self.TID = tid
        self.ADDRESS = address
        self.is_sensor = True if self.TYPE[0] == 'S' else False
        self.is_actuator = True if self.TYPE[0] == 'A' else False
