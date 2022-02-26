from PyQt5.QtGui import QImage, QColor
from PyQt5.QtCore import QPoint, Qt
from Chart import Chart
from View import newPainter
from getSize import *

class Song:
    cover = QImage(1000, 1000, QImage.Format(QImage.Format.Format_RGBA64))
    cover.fill(QColor(0,0,0,128))
    def __init__(self, chart: Chart, illustration: QImage = None):
        self.chart=chart
        self.illustration=illustration.scaled(int(getWidth(800)),int(getHeight(450)),
            transformMode=Qt.TransformationMode.SmoothTransformation)
    
    async def render(self, RTime, painter: newPainter):
        try:
            if self.illustration:
                painter.drawImage(QPoint(0,0),self.illustration)
                painter.drawImage(0,0,self.cover)
            self.chart.render(RTime, painter).send(None)
        except StopIteration: pass
