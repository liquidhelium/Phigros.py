from .Events import Events
from .PhiTime import phiToSecond, secondToPhi


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

    def getFloorAtTime(self, time):
        spEvNow = self.speedEvents.get(time)
        yline = spEvNow[0] + \
            phiToSecond(time - spEvNow[2], self.bpm) * spEvNow[1]
        return yline
