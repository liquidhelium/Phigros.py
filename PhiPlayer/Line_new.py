from PyQt5.QtWidgets import QGraphicsItemGroup, QGraphicsLineItem
from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtCore import QLineF
from .Line import Line
from .Note_new import GuiNote
from .constants import *

class GuiLine(QGraphicsItemGroup):
    def __init__(self, parent, phiLine: Line) -> None:
        super().__init__(parent)
        self.phiLine = phiLine
        self._init_notes()
        self.theLine = QGraphicsLineItem(-1000,0,1000,0)
        self.addToGroup(self.theLine)
    
    def _init_notes(self):
        [self.addToGroup(GuiNote(note)) for note in self.phiLine.notesAbove]
        [self.addToGroup(GuiNote(note, rotated=True)) for note in self.phiLine.notesBelow]
    
    def updateState(self, RTime:float):
        self.state = self.phiLine.getStateAtTime(RTime)
        for note in self.childItems():
            if hasattr(note,"updatePos"):
                note.updatePos(self.state.lineY)
        self.setPos(self.state.pos[0]*SCREEN_WIDTH, self.state.pos[1]*SCREEN_HEIGHT)
        self.setRotation(self.state.angle)


    def paint(self, painter: QPainter,*args) -> None:
        pen = QPen(QColor(171, 170, 103, int(
            255 * self.state.alpha)))
        pen.setWidth(6)
        self.theLine.setPen(pen)
        super().paint(painter, *args)
