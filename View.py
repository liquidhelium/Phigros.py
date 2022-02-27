from PyQt5.QtGui import QPainter
from PyQt5.QtCore import QPointF
from getSize import *

class newPainter(QPainter):
    def __init_subclass__(cls) -> None:
        return super().__init_subclass__()

    def TranslationPhi(painter: QPainter, x: int, y: int):
        class TranslationPhi:

            def __init__(self, phiX, phiY):
                self.X = phiX * getWidth()
                self.Y = phiY * getHeight()

            def __enter__(self):
                painter.translate(QPointF(self.X, self.Y))

            def __exit__(self, type, value, trace):
                painter.translate(QPointF(-self.X, -self.Y))
        return TranslationPhi(x,y)
        
        
    def Rotation(painter:QPainter, angle: int):
        class Rotation:

            def __init__(self, ang):
                self.ang = ang

            def __enter__(self):
                painter.rotate(self.ang)

            def __exit__(self, type, value, trace):
                painter.rotate(-self.ang)
        return Rotation(angle)










