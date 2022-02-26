from bisect import bisect
from PyQt5.QtGui import QImage
from PyQt5.QtCore import QPoint

import Events
from Events import Events
from PhiTime import phiToSecond
from HitAnimation import getHit
from getSize import getHeight, getWidth
from View import newPainter

class Note:
        
    texture_: list[QImage] = [
        None,
        QImage("assets/tap.png"),
        QImage("assets/drag.png"),
        QImage("assets/hold.png"),
        QImage("assets/flick.png")
    ]
    anchors = {
        1:(1,1),
        2:(2,2),
        3:(3,1),
        4:(4,4)
    }

    def __init__(self, type, time, posX, holdTime, speed, floorPos) -> None:
        self.type = type
        self.time = time
        self.posX = posX
        self.holdTime = holdTime
        self.speed = speed
        self.floorPos = floorPos
        self.anchorLabel = Note.anchors[self.type]

    def optmize(self, speedEv,bpm):
        self.realY = self.getRealY(*speedEv.get(self.time).get())
        if self.type == 3:
            spEvTail = speedEv.get(self.time+self.holdTime).get()
            self.tailY =phiToSecond(self.holdTime, bpm) * spEvTail[1]


    def getRealY(self, lastSpdFloor, _, realFloor, __):
        return ((self.floorPos - lastSpdFloor) + realFloor)

    def getRealX(self):
        return (self.posX) / 18 * getHeight(450)

    async def render(self, speedEv: Events, bpm, time, painter: newPainter):
        # we assume that the coordinate is translated.
        y = self.realY
        x = self.getRealX()
        spEvNow = speedEv.get(time).get()
        yline = spEvNow[2] + phiToSecond(time - spEvNow[3], bpm) * spEvNow[1]
        y = (y - yline) * (getHeight(450) / 2)
        if self.type == 3:
            self.texture = Note.texture_[3].scaled(
                int(getWidth(Note.texture_[3].width())),
                int((self.tailY)*getHeight(450)/2)
                )
        else:
            self.texture = Note.texture_[self.type].scaled(
                int(getWidth(Note.texture_[self.type].width())), 
                int(getHeight(Note.texture_[self.type].height()))
                )
        if self.time + self.holdTime >= time:
            an = self.getAnchor()
            painter.drawImage(QPoint(int(x - an[0]),int( y - an[1])), self.texture)
        
        hit = getHit(phiToSecond(self.time - time,bpm)+0.5)
        if hit:
            hit = hit.scaled(int(getWidth(128)), int(getHeight(128)))
            painter.drawImage(QPoint(int(x-hit.width()/2),int(-hit.height()/2)),
                 hit,hit.rect())

    def getAnchor(self):
        return getHeight(Note.texture_[self.anchorLabel[0]].width() / 2),\
               getWidth(Note.texture_[self.anchorLabel[1]].height() / 2)
        

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
