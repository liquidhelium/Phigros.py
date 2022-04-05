from bisect import bisect
from PyQt5.QtGui import QImage, QTransform
from PyQt5.QtCore import Qt

from Line import Line
from PhiTime import phiToSecond
from HitAnimation import HitAnimation


class Note:

    texture_: list[QImage] = [
        None,
        QImage("assets/tap.png").mirrored(False, True),
        QImage("assets/drag.png").mirrored(False, True),
        QImage("assets/hold.png").mirrored(False, True),
        QImage("assets/flick.png").mirrored(False, True)
    ]

    def __init__(self, parent:Line,type, time, posX, holdTime, speed, floorPos) -> None:
        self.parent = parent
        self.textureCache = None
        self.textureCacheRes = (0,0)
        self.type = type
        self.time = time
        self.posX = posX
        self.holdTime = holdTime
        self.speed = speed
        self.floorPos = floorPos
        self.hitAnimations: list[HitAnimation] = []

    def optmize(self, speedEv, bpm):
        self.FloorY = self.getFloorY()
        self.FloorX = self.getFloorX()
        if self.type == 3:
            spEvTail = speedEv.get(self.time+self.holdTime)
            self.tailY = phiToSecond(self.holdTime, bpm) * spEvTail[1]

    def genHit(self, realX, realY, lineX, lineY):
        
        ang = self.parent.getAngleAtTime(phiToSecond(self.time,self.parent.bpm))
        trans =  QTransform()
        trans.translate(lineX,lineY)
        trans.rotate(ang, Qt.Axis.ZAxis)
        self.hitAnimations.append(HitAnimation(phiToSecond(self.time,self.parent.bpm),*trans.map(realX,realY)))
    def getFloorY(self):
        return self.floorPos 

    def getFloorX(self):
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

    def __init__(self, parent: Line, *arg) -> None:
        self.parent = parent
        super().__init__(*arg)

    def getNearNotes(self, time):
        yline = self.parent.getFloorAtTime(time)
        max = bisect(self, yline + 5)
        min = bisect(self, yline - 5)
        return self[min:max]
