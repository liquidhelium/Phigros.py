from bisect import bisect
from PyQt5.QtGui import QImage

import Events
from Events import Events
from PhiTime import phiToSecond
from HitAnimation import getHit


class Note:

    texture_: list[QImage] = [
        None,
        QImage("assets/tap.png").mirrored(False, True),
        QImage("assets/drag.png").mirrored(False, True),
        QImage("assets/hold.png").mirrored(False, True),
        QImage("assets/flick.png").mirrored(False, True)
    ]

    def __init__(self, type, time, posX, holdTime, speed, floorPos) -> None:
        self.type = type
        self.time = time
        self.posX = posX
        self.holdTime = holdTime
        self.speed = speed
        self.floorPos = floorPos

    def optmize(self, speedEv, bpm):
        self.realY = self.getRealY(*speedEv.get(self.time).get())
        if self.type == 3:
            spEvTail = speedEv.get(self.time+self.holdTime).get()
            self.tailY = phiToSecond(self.holdTime, bpm) * spEvTail[1]

    def getRealY(self, lastSpdFloor, _, realFloor, __):
        return ((self.floorPos - lastSpdFloor) + realFloor)

    def getRealX(self):
        return (self.posX) / 18


    def getAnchor(self, img: QImage):
        if self.type == 3:
            return img.width()/2, 5
        else:
            return img.width()/2, img.height()/2
        

    def __lt__(self, other):
        try:
            return self.floorPos < other
        except NotImplementedError:
            return self.floorPos < other.floorPos

    def __gt__(self, other):
        try:
            return self.floorPos > other
        except NotImplementedError:
            return self.floorPos > other.floorPos


class Notes(list[Note]):

    def __init__(self, *arg) -> None:
        super().__init__(*arg)

    def getNearNotes(self, time, speedEv: Events, bpm):
        spEvNow = speedEv.get(time).get()
        yline = spEvNow[2] + phiToSecond(time - spEvNow[3], bpm) * spEvNow[1]
        max = bisect(self, yline + 5)
        min = bisect(self, yline - 5)
        return self[min:max]
