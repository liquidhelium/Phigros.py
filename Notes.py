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
        self.textureCache = None
        self.textureCacheRes = (0,0)
        self.type = type
        self.time = time
        self.posX = posX
        self.holdTime = holdTime
        self.speed = speed
        self.floorPos = floorPos

    def optmize(self, speedEv, bpm):
        self.realY = self.getRealY()
        self.realX = self.getRealX()
        if self.type == 3:
            spEvTail = speedEv.get(self.time+self.holdTime).get()
            self.tailY = phiToSecond(self.holdTime, bpm) * spEvTail[1]

    def getRealY(self):
        return self.floorPos 

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
        yline = spEvNow[0] + phiToSecond(time - spEvNow[2], bpm) * spEvNow[1]
        max = bisect(self, yline + 5)
        min = bisect(self, yline - 5)
        return self[min:max]
