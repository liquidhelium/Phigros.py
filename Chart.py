from Line import Line
from View import newPainter


class Chart:

    def __init__(self, ver, offset, notesCount, lines: list[Line]) -> None:
        self.ver = ver
        self.offset = offset
        self.notesCount = notesCount
        self.lines = lines

    async def render(self, RTime: int, painter: newPainter):
        for line in self.lines:
            try:
                line.render(RTime, painter).send(None)
            except StopIteration:
                pass
