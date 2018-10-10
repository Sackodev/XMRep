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
    def __dir__(self):
        dicc = {}
        if self.type is not None:
            dicc['type'] = hex(self.type)
        if self.pitch is not None:
            dicc['pitch'] = hex(self.pitch)
        if self.ins is not None:
            dicc['ins'] = hex(self.ins)
        if self.vol is not None:
            dicc['vol'] = hex(self.vol)
        if self.fx1 is not None:
            dicc['fx1'] = hex(self.fx1)
        if self.fx2 is not None:
            dicc['fx2'] = hex(self.fx2)
        return [dicc]
