from Line import Line


class Chart:
    def __init__(self, ver, offset, notesCount, lines: list[Line]) -> None:
        self.ver = ver
        self.offset = offset
        self.notesCount = notesCount
        self.lines = lines

    async def render(self,time):
        for line in self.lines:
            try:
                line.render(time).send(None)
            except StopIteration:
                pass


