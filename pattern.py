from channel import Channel

class Pattern(object):
    def __init__(self, pNum, cNum):
        self.pNum = pNum
        self.ch = [Channel() for i in range(cNum)]
