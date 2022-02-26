from PyQt5.QtCore import QPointF
from PyQt5 .QtGui import QImage, QColor

from Events import Events
from PhiTime import secondToPhi
from View import newPainter
from getSize import *

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

    async def render(self, RTime, painter: newPainter):
        time = secondToPhi(RTime, self.bpm)
        posXYEv = self.moveEvents.get(time)
        alphaEv = self.disappearEvents.get(time)
        angleEv = self.rotateEvents.get(time)
        pic = QImage(int(getWidth(2000)), int(getHeight(4)),QImage.Format(QImage.Format.Format_RGBA64))
        pic.fill(QColor(171, 170, 103, int(255 * alphaEv.get(time))))
        with painter.TranslationPhi(*posXYEv.get(time)), \
             painter.Rotation(angleEv.get(time)):
            painter.drawImage(QPointF(-pic.width() / 2, -pic.height() / 2), pic)
            for note in self.notesAbove.getNearNotes(time, self.speedEvents,
                                                     self.bpm):
                try:
                    note.render(self.speedEvents, self.bpm, time, painter).send(None)
                except StopIteration:
                    pass
            with painter.Rotation(180):
                for note in self.notesBelow.getNearNotes(
                        time, self.speedEvents, self.bpm):
                    try:
                        note.render(self.speedEvents, self.bpm,
                                    time, painter).send(None)
                    except StopIteration:
                        pass
