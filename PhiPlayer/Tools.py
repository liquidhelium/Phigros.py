from math import floor
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtCore import QRect
from .View import mapTo
from abc import abstractmethod

from .integrated import IntegratedPlayer


class Tool:
    @classmethod
    @abstractmethod
    def mousePress(cls, event: QMouseEvent,
                   player: IntegratedPlayer) -> None: pass

    @classmethod
    @abstractmethod
    def mouseMove(cls, event: QMouseEvent, player: IntegratedPlayer): pass

    @classmethod
    @abstractmethod
    def mouseRelease(cls, event: QMouseEvent, player: IntegratedPlayer): pass

    @classmethod
    @abstractmethod
    def keyDown(cls, event, player: IntegratedPlayer): pass

    @classmethod
    @abstractmethod
    def keyUp(cls, event, player: IntegratedPlayer): pass


class selectTool(Tool):
    @classmethod
    def mousePress(cls, event: QMouseEvent, player: IntegratedPlayer):
        player.drawr = True
        player.mousePressedPos = event.pos()
        player.selectionBefore = player.selectedObj.copy()

    @classmethod
    def mouseMove(cls, event: QMouseEvent, player: IntegratedPlayer):
        player.mousePressAndMovedPos = event.pos()
        if player.mousePressedPos and player.mousePressAndMovedPos:

            for rect, obj in player.objAndRects:
                # self._debugRend.append(rect) #DEBUG
                # if rect.intersected(QRect(self.mousePressedPos,self.mousePressAndMovedPos)).contains(rect): # 全部进入才算选择
                # 有交集就算选择
                if rect.intersects(QRect(player.mousePressedPos, player.mousePressAndMovedPos)):
                    if player.ShiftPressed and (obj in player.selectionBefore):
                        if obj in player.selectedObj:
                            player.selectedObj.remove(obj)
                    else:
                        player.selectedObj |= set([obj])
                elif (obj in player.selectedObj):
                    if player.ShiftPressed and obj in player.selectionBefore:
                        player.selectedObj |= set([obj])
                    else:
                        player.selectedObj.remove(obj)
                elif (obj in player.selectionBefore) and player.ShiftPressed:
                    player.selectedObj |= set([obj])
            player.update()

    @classmethod
    def mouseRelease(cls, event: QMouseEvent, player: IntegratedPlayer):
        player.mousePressedPos = None
        player.mousePressAndMovedPos = None
        player.selectionBefore = player.selectedObj.copy()
        player.update()


class moveTool(Tool):
    @classmethod
    def mousePress(cls, event: QMouseEvent, player) -> None:
        player.drawr = False
        for rect, obj in player.objAndRects:
            if rect.contains(event.pos()):
                player.mousePressedPos = event.pos()
                break
            else:
                player.mousePressedPos = None
        for obj in player.selectedObj:
            obj.lastFloorX = obj.FloorX
            obj.lastFloorY = obj.FloorY

    @classmethod
    def mouseMove(cls, event: QMouseEvent, player: IntegratedPlayer):
        player.mousePressAndMovedPos = event.pos()
        if player.mousePressedPos and player.mousePressAndMovedPos:
            w = player.width()
            h = player.height()
            for obj in player.selectedObj:
                symbol = -1 if obj.isBelow else 1
                RTime = player.getchartRTime()
                pressAndMoveInLine = mapTo(
                    obj.parent, player.mousePressAndMovedPos, RTime,w,h)
                pressInLine = mapTo(obj.parent, player.mousePressedPos, RTime,w,h)
                obj.FloorX = (floor(symbol*(pressAndMoveInLine.x()-pressInLine.x())
                              / player.width()/player.snip+0.5))*player.snip + obj.lastFloorX
                obj.FloorY = (floor(-symbol*(pressAndMoveInLine.y()-pressInLine.y())
                              / (0.5*player.height())/player.snip+0.5))*player.snip + obj.lastFloorY
                obj.time = obj.parent.getTimeForFloor(obj.FloorY)
                player.update()

    @classmethod
    def mouseRelease(cls, event: QMouseEvent, player: IntegratedPlayer):
        player.mousePressedPos = None
        player.mousePressAndMovedPos = None
        for obj in player.selectedObj:
            obj.genHit()
        player.update()
