from .integrated import IntegratedPlayer
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtCore import Qt
from .Tools import Tool, selectTool, moveTool


class EditablePlayer(IntegratedPlayer):
    def __init__(self, *args) -> None:
        super().__init__(*args)
        self.tool: Tool = selectTool

    def mousePressEvent(self, a0) -> None:
        return self.tool.mousePress(a0, self)

    def mouseMoveEvent(self, a0) -> None:
        return self.tool.mouseMove(a0, self)

    def mouseReleaseEvent(self, a0) -> None:
        return self.tool.mouseRelease(a0, self)

    def keyPressEvent(self, a0: QKeyEvent) -> None:
        if a0.key() == Qt.Key.Key_S:
            self.tool = selectTool
        elif a0.key() == Qt.Key.Key_M:
            self.tool = moveTool
        else:
            super().keyPressEvent(a0)
