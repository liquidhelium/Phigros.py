from .Events import Events
from .PhiTime import phiToSecond, secondToPhi


class LineState:
    def __init__(self, alpha: int, pos: tuple[float,float], angle: float, lineY: float):
        self.alpha = alpha
        self.pos = pos
        self.angle = angle
        self.lineY = lineY

class Line:

    def __init__(self, notesAbove, notesBelow, bpm: int, speedEvents: Events,
                 disappearEvents: Events, moveEvents: Events,
                 rotateEvents: Events):
        self.bpm = bpm
        self.notesAbove = notesAbove
        self.notesBelow = notesBelow
        self.speedEvents = speedEvents
        self.disappearEvents = disappearEvents
        self.moveEvents = moveEvents
        self.rotateEvents = rotateEvents

    def getPosAtTime(self, RTime):
        time = secondToPhi(RTime, self.bpm)
        posXY = self.moveEvents.get(time)
        return posXY

    def getAngleAtTime(self, RTime):
        time = secondToPhi(RTime, self.bpm)
        angle = self.rotateEvents.get(time)
        return angle

    def getAlphaAtTime(self, RTime):
        time = secondToPhi(RTime, self.bpm)
        return self.disappearEvents.get(time)

    def getFloorAtTime2(self, time): # 废弃
        spEvNow = self.speedEvents.get(time)
        yline = spEvNow[0] + \
            phiToSecond(time - spEvNow[2], self.bpm) * spEvNow[1]
        return yline

    def getFloorAtTime(self, RTime):
        time = secondToPhi(RTime, self.bpm)
        spEvNow = self.speedEvents.get(time)
        yline = spEvNow[0] + \
            phiToSecond(time - spEvNow[2], self.bpm) * spEvNow[1]
        return yline

    
    def getTimeForFloor(self, floor:float)-> float:
        spEv = self.speedEvents.bisectForFloor(floor)
        if spEv.value == 0: # avoid zero division
            return spEv.startTime
        else:
            second =  (floor - spEv.floorPos) / spEv.value
            return secondToPhi(second, self.bpm) + spEv.startTime
    
    def getStateAtTime(self, time: float) -> LineState:
        return LineState(
            self.getAlphaAtTime(time),
            self.getPosAtTime(time),
            self.getAngleAtTime(time),
            self.getFloorAtTime(time)
        )

