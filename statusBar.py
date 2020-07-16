class StatusBar:
    def __init__(self, start, final, top):
        self.start = start
        self.final = final
        self.len = self.final - self.start
        self.curpos = 0
        self.top = top
        self.sbp = "B"
        self.delayS = 2
        self.delayF = 0
        self.show = False
        self.tm = 0