from bisect import bisect

import pyglet.image
from pyglet.image import ImageData

import Events
import Properties as prop
from Events import Events
from PhiTime import phiToSecond
from HitAnimation import getHit

class Note:
    texture: list[ImageData] = [
        None,
        pyglet.image.load("assets/tap.png"),
        pyglet.image.load("assets/drag.png"),
        pyglet.image.load("assets/hold.png"),
        pyglet.image.load("assets/flick.png")
    ]
    anchors = [
        None,
        (texture[1].width / 2, texture[1].height / 2),
        (texture[2].width / 2, texture[2].height / 2),
        (texture[3].width / 2, texture[1].height / 2),
        (texture[4].width / 2, texture[4].height / 2),
    ]

    def __init__(self, type, time, posX, holdTime, speed, floorPos) -> None:
        self.type = type
        self.time = time
        self.posX = posX
        self.holdTime = holdTime
        self.speed = speed
        self.floorPos = floorPos

    def optmize(self, speedEv,bpm):
        self.realY = self.getRealY(*speedEv.get(self.time).get())
        self.realX = self.getRealX()
        if self.type == 3:
            spEvTail = speedEv.get(self.time+self.holdTime).get()
            self.tailY =phiToSecond(self.holdTime, bpm) * spEvTail[1]
            self.texture = Note.texture[3].get_texture()
        else:
            self.texture = Note.texture[self.type].get_texture()

    def getRealY(self, lastSpdFloor, _, realFloor, __):
        return ((self.floorPos - lastSpdFloor) + realFloor)

    def getRealX(self):
        return (self.posX) / 18 * prop.screenWidth

    async def render(self, speedEv: Events, bpm, time):
        # we assume that the coordinate is translated.
        y = self.realY
        x = self.realX
        spEvNow = speedEv.get(time).get()
        yline = spEvNow[2] + phiToSecond(time - spEvNow[3], bpm) * spEvNow[1]
        y = (y - yline) * (prop.screenHeight / 2)
        if self.type == 3:
            self.texture.height = int((self.tailY)*prop.screenHeight/2)
        if self.time + self.holdTime >= time:
            self.texture.blit(x - self.anchors[self.type][0],
                                         y - self.anchors[self.type][1])
        hit = getHit(phiToSecond(self.time - time,bpm)+0.5)
        if hit:
            hit.height = 128
            hit.width = 128
            hit.blit(x-64,-64)

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