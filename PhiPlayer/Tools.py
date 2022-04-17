from PyQt5.QtGui import QMouseEvent
from PyQt5.QtCore import QRect
from abc import abstractmethod


class Tool:
    @classmethod
    @abstractmethod
    def mousePress(cls, event: QMouseEvent, player) -> None: pass

    @classmethod
    @abstractmethod
    def mouseMove(cls, event: QMouseEvent, player): pass

    @classmethod
    @abstractmethod
    def mouseRelease(cls, event: QMouseEvent, player): pass

    @classmethod
    @abstractmethod
    def keyDown(cls,event,player): pass

    @classmethod
    @abstractmethod
    def keyUp(cls,event,player): pass


class selectTool(Tool):
    @classmethod
    def mousePress(cls, event: QMouseEvent, player):
        player.mousePressedPos = event.pos()
        player.selectionBefore = player.selectedObj.copy()


    @classmethod
    def mouseMove(cls, event: QMouseEvent, player):
        player.mousePressAndMovedPos = event.pos()
        if player.mousePressedPos and player.mousePressAndMovedPos:
            
            for rect, obj in player.objAndRects:
                # self._debugRend.append(rect) #DEBUG
                # if rect.intersected(QRect(self.mousePressedPos,self.mousePressAndMovedPos)).contains(rect): # 全部进入才算选择
                if rect.intersects(QRect(player.mousePressedPos,player.mousePressAndMovedPos)): # 有交集就算选择
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
    def mouseRelease(cls, event: QMouseEvent, player):
        player.mousePressedPos = None
        player.mousePressAndMovedPos = None
        player.selectionBefore = player.selectedObj.copy()
        player.update()