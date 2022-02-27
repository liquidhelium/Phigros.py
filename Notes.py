from bisect import bisect
from PyQt5.QtGui import QImage
from PyQt5.QtCore import QPoint, Qt, QRect

import Events
from Events import Events
from PhiTime import phiToSecond
from HitAnimation import getHit
from getSize import getHeight, getWidth
from View import newPainter


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
        return (self.posX) / 9 * getHeight(450)

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
                int((self.tailY)*getHeight(450)/2),
                transformMode=Qt.TransformationMode.SmoothTransformation
            )
            # self.texture = self.texture.copy(QRect(0,256,
            #         256,256))
        else:
            self.texture = Note.texture_[self.type].scaled(
                int(getWidth(100)),
                int(getHeight(Note.texture_[self.type].height()
                              * 100/Note.texture_[self.type].width())),
                transformMode=Qt.TransformationMode.SmoothTransformation
            )
        an = self.getAnchor(self.texture)
        drawRect = QRect(0, int(-y),
                         self.texture.width(), int(self.texture.height()+y))

        if self.time + self.holdTime >= time:

            painter.drawImage(
                QPoint(int(x - an[0]), int(- an[1])), self.texture, drawRect)

        hit = getHit(phiToSecond(self.time - time, bpm)+0.5)
        if hit:
            hit = hit.scaled(int(getWidth(128)), int(getHeight(128)),
                             transformMode=Qt.TransformationMode.SmoothTransformation
                             )
            painter.drawImage(QPoint(int(x-hit.width()/2), int(-hit.height()/2)),
                              hit, hit.rect())

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
