import virtualenv
from Line import Line


class Chart:
    def __init__(self, version, offset, notesCount, lines: list[Line]) -> None:
        self.version = version
        self.offset = offset
        self.notesCount = notesCount
        self.lines = lines

    def render(self):
        for line in self.lines:
            line.render()