from PyQt5.QtGui import QPainter, QImage, QColor
from PyQt5.QtCore import QPointF, Qt, QRect, QPoint
from Chart import Chart
from Events import Events
from HitAnimation import getHit
from Notes import Note
from PhiTime import phiToSecond, secondToPhi
from Song import Song
from Line import Line

class newPainter(QPainter):
    def __init__(self, *args):
        super().__init__(*args)

    def TranslationPhi(painter: QPainter, x: int, y: int):
        class TranslationPhi:

            def __init__(self, phiX, phiY):
                self.X = phiX * painter.getWidthForPercent()
                self.Y = phiY * painter.getHeightForPercent()

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

    def getHeightForPercent(self, heightWant: float=1):
        return (heightWant) * self.device().height()

    def getWidthForPercent(self, widthWant: float=1):
        return (widthWant) * self.device().width()

    def drawSong(self, RTime: float, song: Song):
        try:
            if song.illustration:
                self.drawImage(0,0,
                    song.illustration.scaled(
                        int(self.getWidthForPercent(1)),
                        int(self.getHeightForPercent(1)),
                transformMode=Qt.TransformationMode.SmoothTransformation)
                )
                self.drawImage(0,0,song.cover.scaled(
                    int(self.getWidthForPercent(1)),
                    int(self.getHeightForPercent(1))))
            self.drawChart(RTime, song.chart).send(None)
        except StopIteration: 
            self.device().needGenTexture = False
            pass

        
    async def drawChart(self, RTime: float, chart: Chart):
            for line in chart.lines:
                try:
                    self.drawJudgeLine(RTime, line).send(None)
                except StopIteration:
                    pass
    
    
    async def drawJudgeLine(self, RTime, line: Line):
        time = secondToPhi(RTime, line.bpm)
        posXYEv = line.moveEvents.get(time)
        alphaEv = line.disappearEvents.get(time)
        angleEv = line.rotateEvents.get(time)
        pic = QImage(int(self.getWidthForPercent(3)), 
                    int(self.getHeightForPercent(0.01)),
                    QImage.Format(QImage.Format.Format_RGBA64))
        pic.fill(QColor(171, 170, 103, int(255 * alphaEv.get(time))))
        with self.TranslationPhi(*posXYEv.get(time)), \
             self.Rotation(angleEv.get(time)):
            self.drawImage(QPointF(-pic.width() / 2, -pic.height() / 2), pic)
            for note in line.notesAbove.getNearNotes(time, line.speedEvents,
                                                     line.bpm):
                try:
                    self.drawNote(line.speedEvents, line.bpm, time, note).send(None)
                except StopIteration:
                    pass
            with self.Rotation(180):
                for note in line.notesBelow.getNearNotes(
                        time, line.speedEvents, line.bpm):
                    try:
                        self.drawNote(line.speedEvents, line.bpm,
                                    time, note).send(None)
                    except StopIteration:
                        pass

    async def drawNote(self, speedEv: Events, bpm, time, note: Note):
        # we assume that the coordinate is translated.
        y = note.realY
        x = self.getWidthForPercent(note.getRealX())
        spEvNow = speedEv.get(time).get()
        yline = spEvNow[2] + phiToSecond(time - spEvNow[3], bpm) * spEvNow[1]
        y = (y - yline) * (self.getHeightForPercent(1) / 2)
        if not (note.textureCacheRes == self.device().size and note.textureCache):
            if note.type == 3:
                texture = Note.texture_[3].scaled(
                    int(self.getWidthForPercent(Note.texture_[3].width()/800)),
                    int((note.tailY)*self.getHeightForPercent(1)/2),
                    transformMode= Qt.TransformationMode.SmoothTransformation
                )
            else:
                texture = Note.texture_[note.type].scaled(
                    int(self.getWidthForPercent(1/8)),
                    int(self.getHeightForPercent((Note.texture_[note.type].height()
                                * 100/Note.texture_[note.type].width())/450)),
                    transformMode= Qt.TransformationMode.SmoothTransformation
                )
            note.textureCacheRes = self.device().size
            note.textureCache = texture
        else:
            texture = note.textureCache
        an = note.getAnchor(texture)
        drawRect = QRect(0, int(-y),
                         texture.width(), 
                         int(texture.height()+y))

        if note.time + note.holdTime >= time:

            self.drawImage(
                QPoint(int(x - an[0]), 
                int(- an[1])),
                texture, 
                drawRect
            )

        hit = getHit(phiToSecond(note.time - time, bpm)+0.5)
        if hit:
            hit = hit.scaled(
                int(self.getWidthForPercent(0.15)), 
                int(self.getWidthForPercent(0.15)),
            )
            self.drawImage(
                QPoint(int(x-hit.width()/2), 
                int(-hit.height()/2)),
                hit, hit.rect())






