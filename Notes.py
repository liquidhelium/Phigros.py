from bisect import bisect
import pyglet.image
from pyglet.image import ImageData

import Events
from Events import Events
from PhiTime import phiToSecond
from HitAnimation import getHit
from getSize import getHeight, getWidth

class Note:
    
        
    texture: list[ImageData] = [
        None,
        pyglet.image.load("assets/tap.png"),
        pyglet.image.load("assets/drag.png"),
        pyglet.image.load("assets/hold.png"),
        pyglet.image.load("assets/flick.png")
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
            self.texture = Note.texture[3].get_texture()
        else:
            self.texture = Note.texture[self.type].get_texture()

    def getRealY(self, lastSpdFloor, _, realFloor, __):
        return ((self.floorPos - lastSpdFloor) + realFloor)

    def getRealX(self):
        return (self.posX) / 18 * getHeight(450)

    async def render(self, speedEv: Events, bpm, time):
        # we assume that the coordinate is translated.
        y = self.realY
        x = self.getRealX()
        spEvNow = speedEv.get(time).get()
        yline = spEvNow[2] + phiToSecond(time - spEvNow[3], bpm) * spEvNow[1]
        y = (y - yline) * (getHeight(450) / 2)
        if self.type == 3:
            self.texture.height = int((self.tailY)*getHeight(450)/2)
        if self.time + self.holdTime >= time:
            an = self.getAnchor()
            self.texture.blit(x - an[0], y - an[1])
        hit = getHit(phiToSecond(self.time - time,bpm)+0.5)
        if hit:
            hit.height = getHeight(128)
            hit.width = getWidth(128)
            hit.blit(x-hit.width//2,-hit.height//2)

    def getAnchor(self):
        return getHeight(Note.texture[self.anchorLabel[0]].width / 2),\
               getWidth(Note.texture[self.anchorLabel[1]].height / 2)
        

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
