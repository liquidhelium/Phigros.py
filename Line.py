import pyglet.graphics
import pyglet.image
import pyglet.sprite

from Events import Events
from View import Rotation, TranslationPhi


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

    def render(self, time):
        posXYEv = self.moveEvents.get(time)
        alphaEv = self.disappearEvents.get(time)
        angleEv = self.rotateEvents.get(time)
        pic = pyglet.image.create(
            2000, 4,
            pyglet.image.SolidColorImagePattern(
                (171, 170, 103, int(255 * alphaEv.get(time)))))
        with TranslationPhi(*posXYEv.get(time)), Rotation(angleEv.get(time)):
            pic.blit(-pic.width / 2, -pic.height / 2)
            for note in self.notesAbove.getNearNotes(time, self.speedEvents,
                                                     self.bpm):
                note.render(self.speedEvents, self.bpm, time)
            with Rotation(180):
                for note in self.notesBelow.getNearNotes(
                        time, self.speedEvents, self.bpm):
                    note.render(self.speedEvents, self.bpm,
                                    time)
