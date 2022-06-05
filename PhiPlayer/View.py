from PyQt5.QtGui import QPainter, QColor, QPen, QBrush, QFont, QFontMetricsF, QPixmap
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsPixmapItem, QGraphicsBlurEffect
from PyQt5.QtCore import QPointF, Qt, QRect, QPoint, QRectF
from .Chart import Chart
from .Events import Events
from .HitAnimation import getHit
from .Notes import Note
from .PhiTime import phiToSecond, secondToPhi
from .Song import Song
from .Line import Line


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
        return TranslationPhi(x, y)

    def Rotation(painter: QPainter, angle: int):
        class Rotation:

            def __init__(self, ang):
                self.ang = ang

            def __enter__(self):
                painter.rotate(self.ang)

            def __exit__(self, type, value, trace):
                painter.rotate(-self.ang)
        return Rotation(angle)

    def getHeightForPercent(self, heightWant: float = 1):
        return (heightWant) * self.device().height()

    def getWidthForPercent(self, widthWant: float = 1):
        return (widthWant) * self.device().width()

    def drawStatus(self):
        self.resetTransform()
        self.setBrush(QColor(220, 220, 220))
        self.setPen(QColor(220, 220, 220))
        font = QFont("微软雅黑", int(self.getHeightForPercent(0.025)),
                     int(self.getHeightForPercent(0.0031)))
        self.setFont(font)
        fm = QFontMetricsF(font)
        bottomMarglin = 0.035
        sideMarglin = 0.035
        bottomY = self.device().height()-self.getHeightForPercent(bottomMarglin)
        self.drawText(QPointF(self.getHeightForPercent(
            sideMarglin+0.0165), bottomY), "Introduction")
        self.drawRect(QRectF(
            self.getHeightForPercent(sideMarglin),
            bottomY-fm.capHeight()*1.1,
            self.getHeightForPercent(0.008),
            fm.capHeight()*1.2
        ))
        levelString = "EZ  Lv.2"
        self.drawText(QPointF(self.device().width(
        ) - self.getHeightForPercent(sideMarglin) - fm.width(levelString), bottomY), levelString)

    def drawSong(self, RTime: float, song: Song):
        if song.illustration:
            if not (song.illustrationCacheRes == self.device().size()
                    and song.illustrationCache):
                ill = song.illustration.scaled(
                    int(self.getWidthForPercent(1)),
                    int(self.getHeightForPercent(1)),
                    transformMode=Qt.TransformationMode.SmoothTransformation)
                scene = QGraphicsScene()
                item = QGraphicsPixmapItem()
                item.setPixmap(ill)
                eff = QGraphicsBlurEffect()
                eff.setBlurRadius(10)
                item.setGraphicsEffect(eff)
                scene.addItem(item)
                song.illustrationCache = scene
                song.illustrationCacheRes = self.device().size()
            song.illustrationCache.render(self)

            if not (song.coverCacheRes == self.device().size()
                    and song.coverCache):
                song.coverCache = song.cover.scaled(
                    int(self.getWidthForPercent(1)),
                    int(self.getHeightForPercent(1)))
                song.coverCacheRes = self.device().size()
            self.drawPixmap(0, 0, song.coverCache)
        self.device().objAndRects = []
        self.drawChart(RTime, song.chart)

    def drawChart(self, RTime: float, chart: Chart):
        for line in chart.lines:
            self.drawJudgeLine(RTime, line)

    def drawJudgeLine(self, RTime, line: Line):
        time = secondToPhi(RTime, line.bpm)
        pen = QPen(QColor(171, 170, 103, int(
            255 * line.getAlphaAtTime(RTime))))
        pen.setWidth(int(self.getHeightForPercent(0.01)))
        self.setPen(pen)

        with self.TranslationPhi(*line.getPosAtTime(RTime)), \
                self.Rotation(line.getAngleAtTime(RTime)):
            self.drawLine(int(self.getWidthForPercent(-1)), 0,
                          int(self.getWidthForPercent(1)), 0)
            for note in line.notesAbove.getNearNotes(time):
                self.drawNote(time, note)
            with self.Rotation(180):
                for note in line.notesBelow.getNearNotes(time):
                    self.drawNote(time, note)

        for note in line.notesAbove.getNearNotes(time):
            self.drawHit(time, note)
        for note in line.notesBelow.getNearNotes(time):
            self.drawHit(time, note)

    def drawNote(self, time, note: Note):
        # we assume that the coordinate is translated.
        x = self.getWidthForPercent(note.FloorX)
        yline = note.parent.getFloorAtTime2(time)
        if not (note.textureCacheRes == self.device().size() and note.textureCache):
            if note.type == 3:
                texture = note.texture_[3].scaled(
                    int(self.getWidthForPercent(note.texture_[3].width()/800)),
                    int((note.tailY)*self.getHeightForPercent(1)/2),
                    transformMode=Qt.TransformationMode.SmoothTransformation
                )
            else:
                texture = note.texture_[note.type].scaled(
                    int(self.getWidthForPercent(1/8)),
                    int(self.getHeightForPercent((note.texture_[note.type].height()
                                                  * 100/note.texture_[note.type].width())/450)),
                    transformMode=Qt.TransformationMode.SmoothTransformation
                )
            note.textureCacheRes = self.device().size()
            note.textureCache = texture
        else:
            texture = note.textureCache
        an = note.getAnchor(texture)
        realY = self.getHeightForPercent((note.FloorY - yline)/2)
        drawRect = QRect(0, int(-realY),
                         texture.width(),
                         int(texture.height()+realY))

        if note.time + note.holdTime >= time:

            self.drawPixmap(
                QPoint(int(x - an[0]),
                       int(- an[1])),
                texture,
                drawRect
            )

            noteRect = QRect(int(x-an[0]-2), int(max(realY-an[1], -2)),
                             texture.width()+4,
                             int(min(texture.height()+4, texture.height()+4+realY)))
            self.device().objAndRects.append((self.worldTransform().mapRect(noteRect), note))
            if note in self.device().selectedObj:
                self.save()
                pen = QPen(QColor(85, 230, 90))
                pen.setWidth(3)
                self.setBrush(QColor(82, 115, 255, 150))
                self.setPen(pen)
                self.drawRect(noteRect)
                self.restore()

    def drawHit(self, time, note: Note):

        x = self.getWidthForPercent(note.FloorX)
        if not (note.hitRes == self.device().size() and note.hitAnimations):

            note.genHit()

            note.hitRes = self.device().size()
        for hit in note.hitAnimations:
            hit.updateTime(phiToSecond(time, note.parent.bpm))
            texture: QPixmap = hit.getTexture()

            if texture:
                texture = texture.scaled(
                    int(self.getWidthForPercent(0.2)),
                    int(self.getWidthForPercent(0.2)),
                    transformMode=Qt.TransformationMode.SmoothTransformation
                )

                self.drawPixmap(QPointF(self.getWidthForPercent(
                    hit.x)-texture.width()//2, self.getHeightForPercent(hit.y)-texture.height()//2), texture)

            particles = hit.genParticles(0.2)

            if particles:
                self.save()
                pen = self.pen()
                pen.setWidth(int(self.getWidthForPercent(0.02)))
                color = pen.color()
                color.setAlpha(int((1-hit.getPercent())*255))
                pen.setColor(color)
                self.setPen(pen)
                for p in particles:
                    self.drawPoint(QPointF(self.getWidthForPercent(
                        p[0]), self.getHeightForPercent(p[1])))
                self.restore()
            # self.drawEllipse(QPoint(hit.x,hit.y),500,500)
