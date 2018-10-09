class Note(object):
    def __init__(self, t):
        self.type = t
        self.isNote = False
        self.isStop = False
        self.pitch = None
        self.ins = None
        self.vol = None
        self.fx1 = None
        self.fx2 = None
