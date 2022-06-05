from PyQt5.QtWidgets import QGraphicsPixmapItem
from PyQt5.QtGui import QPixmap, QPainter


from .Notes import Note
from .constants import *


def makeHold(holdHead: QPixmap, holdBody: QPixmap, holdTail: QPixmap, holdLen: int) -> QPixmap:
    target = QPixmap(NOTE_WIDTH, int(
        holdLen/NOTE_SCALE + HOLD_HEADTAIL_HEIGHT*2))
    painter = QPainter(target)
    painter.drawPixmap(0, 0, holdTail)
    painter.drawPixmap(0, HOLD_HEADTAIL_HEIGHT,
                       holdBody.scaled(NOTE_WIDTH, int(holdLen/NOTE_SCALE)))  # TODO smooth
    painter.drawPixmap(0, HOLD_HEADTAIL_HEIGHT +
                       int(holdLen/NOTE_SCALE), holdHead)
    return target


class GuiNote(QGraphicsPixmapItem):
    texture_: tuple[QPixmap] = (
        QPixmap("./assets/tap.png"),
        QPixmap("./assets/drag.png"),
        None,
        QPixmap("./assets/flick.png"),
    )
    holdTexture_: tuple[QPixmap] = (
        QPixmap("./assets/HoldHead.png"),
        QPixmap("./assets/HoldBody.png"),
        QPixmap("./assets/HoldEnd.png")
    )

    def __init__(self, phiNote: Note, rotated: bool = False):
        super().__init__()
        self.phiNote = phiNote
        if phiNote.type == 3:
            self.setPixmap(makeHold(*GuiNote.holdTexture_,
                           (phiNote.getTailY())*SCREEN_HEIGHT))
            self.setTransformOriginPoint(-NOTE_WIDTH/2,
                                         -self.pixmap().height()/2)
            
        else:
            # 1,2,3,4 -> 0,1,2,3
            self.setPixmap(GuiNote.texture_[self.phiNote.type - 1])
            self.setTransformOriginPoint(-NOTE_WIDTH /
                                         2, -self.pixmap().height()/2)
        if rotated:
            self.setRotation(180)
        self.setScale(NOTE_SCALE)
        self.ySymbol = -2*rotated + 1  # 0 -> 1, 1 -> -1

    def updatePos(self, lineY: float):
        self.setPos(self.phiNote.getFloorX()*SCREEN_WIDTH,
                    self.ySymbol*(self.phiNote.getFloorY()-lineY)*SCREEN_HEIGHT/2)
