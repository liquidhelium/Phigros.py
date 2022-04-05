from PyQt5.QtGui import QPainter, QImage, QColor, QPen, QBrush, QPalette
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
        if song.illustration:
            if not (song.illustrationCacheRes == self.device().size 
                and song.illustrationCache):
                song.illustrationCache = song.illustration.scaled(
                    int(self.getWidthForPercent(1)),
                    int(self.getHeightForPercent(1)),
                    transformMode=Qt.TransformationMode.SmoothTransformation)
                song.illustrationCacheRes = self.device().size
            self.drawImage(0, 0, song.illustrationCache)
            if not (song.coverCacheRes == self.device().size 
                and song.coverCache):
                song.coverCache = song.cover.scaled(
                    int(self.getWidthForPercent(1)),
                    int(self.getHeightForPercent(1)))
                song.coverCacheRes = self.device().size
            self.drawImage(0,0,song.coverCache)
        self.device().objAndRects = []
        self.drawChart(RTime, song.chart)

        
    def drawChart(self, RTime: float, chart: Chart):
        for line in chart.lines:
            self.drawJudgeLine(RTime, line)
    
    
    def drawJudgeLine(self, RTime, line: Line):
        time = secondToPhi(RTime, line.bpm)
        pen = QPen(QColor(171, 170, 103, int(255 * line.getAlphaAtTime(RTime))))
        pen.setWidth(self.getHeightForPercent(0.01))
        self.setPen(pen)

        with self.TranslationPhi(*line.getPosAtTime(RTime)), \
             self.Rotation(line.getAngleAtTime(RTime)):
            self.drawLine(int(self.getWidthForPercent(-1)),0,int(self.getWidthForPercent(1)),0)
            self.drawEllipse(QPoint(0,0), 10, 10)
            for note in line.notesAbove.getNearNotes(time):
                self.drawNote(time, note)
            with self.Rotation(180):
                for note in line.notesBelow.getNearNotes(time):
                    self.drawNote(time, note)
        for note in line.notesAbove.getNearNotes(time):
                self.drawHit(time, note)
        with self.Rotation(180):
            for note in line.notesBelow.getNearNotes(time):
                self.drawHit(time, note)

    def drawNote(self, time, note: Note):
        # we assume that the coordinate is translated.
        x = self.getWidthForPercent(note.FloorX)
        yline = note.parent.getFloorAtTime(time)
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
        realY = self.getHeightForPercent((note.FloorY - yline)/2)
        drawRect = QRect(0, int(-realY), 
                         texture.width(), 
                         int(texture.height()+realY))

        if note.time + note.holdTime >= time:

            self.drawImage(
                QPoint(int(x - an[0]), 
                int(- an[1])),
                texture, 
                drawRect
            )
            
            
            noteRect =  QRect(int(x-an[0]-2), int(max(realY-an[1],-2)), 
                         texture.width()+4, 
                         int(min(texture.height()+4,texture.height()+4+realY)))
            self.device().objAndRects.append((self.worldTransform().mapRect(noteRect),note))
            if self.device().selectedObj is note:
                self.save()
                pen = QPen(QColor(85, 230, 90))
                pen.setWidth(3)
                self.setBrush(QColor(82,115,255,150))
                self.setPen(pen)
                self.drawRect(noteRect)
                self.restore()
    
    def drawHit(self, time, note):
        
        x = self.getWidthForPercent(note.FloorX)
        if not (note.textureCacheRes == self.device().size and note.hitAnimations):
            pos = note.parent.getPosAtTime(phiToSecond(note.time+1,note.parent.bpm)) 

            note.genHit(int(x),int(0),pos[0]*self.getWidthForPercent(),pos[1]*self.getHeightForPercent())
        for hit in note.hitAnimations:
            hit.updateTime(phiToSecond(time,note.parent.bpm))
            texture = hit.getTexture()
            
            
            if texture:
                texture = texture.scaled(
                    int(self.getWidthForPercent(0.15)), 
                    int(self.getWidthForPercent(0.15)),
                )
                
                
                self.drawImage(QPoint(hit.x-texture.width()//2,hit.y-texture.height()//2),texture)
            # self.drawEllipse(QPoint(hit.x,hit.y),500,500)






