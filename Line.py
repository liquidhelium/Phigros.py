import pyglet.sprite
from pyglet.image import AbstractImage
import pyglet.graphics
import pyglet.image
import View
from Events import Events


class Line:

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
        alpha = self.disappearEvents.get(time)[0]
        angle = self.rotateEvents.get(time)[0]
        pic = pyglet.image.create(2000,4,
            pyglet.image.SolidColorImagePattern((171,170,103,int(255*alpha))))
        View.draw(pic, *posXY, ang=angle)


