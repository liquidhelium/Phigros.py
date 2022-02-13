import pyglet.sprite
from pyglet.image import AbstractImage
import pyglet.graphics
import View
from Events import Events


class Line:
    texture: AbstractImage = pyglet.image.load("assets/line.png")
    textureMask: AbstractImage = pyglet.image.load("assets/line_empty.png")

    def __init__(self, notesAbove, notesBelow, 
                # bpm: int,
                speedEvents: Events,
                disappearEvents: Events,
                moveEvents: Events,
                rotateEvents: Events):
        # self.bpm = bpm
        self.notesAbove = notesAbove
        self.notesBelow = notesBelow
        self.speedEvents = speedEvents
        self.disappearEvents = disappearEvents
        self.moveEvents = moveEvents
        self.rotateEvents = rotateEvents


    async def render(self, time):
        posXY = self.moveEvents.get(time)
        print(posXY)
        alpha = self.disappearEvents.get(time)[0]
        angle = self.rotateEvents.get(time)[0]
        View.draw(Line.textureMask, *posXY, ang=angle)


