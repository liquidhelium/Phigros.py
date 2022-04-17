from .integrated import IntegratedPlayer
from .Tools import Tool, selectTool

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

