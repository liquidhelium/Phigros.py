
import time
from typing import Any, Union
from warnings import warn

from PyQt5.QtCore import pyqtSignal, QUrl, QRect, QPoint, Qt
from PyQt5.QtGui import QImage, QResizeEvent, QMouseEvent, QPixmap, QTransform, QColor, QKeyEvent
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from .Notes import Note

from .officalChartLoader import officalChartLoader
from .Song import Song
from .View import newPainter



class IntegratedPlayer(QWidget):

    timeUpdate = pyqtSignal(int)
    rangeLoaded = pyqtSignal(int, int)
    endTimeLoaded = pyqtSignal(int)
    toogled = pyqtSignal() 
    bePaused = pyqtSignal()
    bePlayed = pyqtSignal()
    

    def __init__(self, parent) -> None:

        super().__init__(parent)
        from .HitAnimation import init
        init()
        self.startTime = time.perf_counter()
        self.now = self.startTime
        self.paused = False
        self.pausedAt = 0
        self.fps = 0
        self.fpstimer = self.startTimer(500)
        self.objAndRects: list[tuple[QRect,Any]] = []
        self.selectedObj: set[Note] = set()
        self.selectionBefore: set[Note] = set()
        self.timer: Union[int, None] = None
        self.musicPlayer = QMediaPlayer(self)   
        self.TRANSLATION = QTransform()
        self.TRANSLATION.rotate(180,Qt.Axis.XAxis)
        self.mousePressedPos = None
        self.mousePressAndMovedPos = None
        self.ShiftPressed = False
        self.drawr = True
        self.fpsPrint = 0
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        # self._debugRend = [] # DEBUG
        self.pause()
 

    def start(self):
        if self.paused:
            # avoid duplicate defining
            self.timer = self.startTimer(int(100/6)+1) if not self.timer else self.timer
            self.now = time.perf_counter()
            self.startTime = self.now-self.pausedAt
            self.musicPlayer.play()
            self.paused = False
            self.bePlayed.emit()
            self.pausedAt = 0

    def pause(self):
        if not self.paused:
            if self.timer:
                self.killTimer(self.timer)
                self.timer = None
            self.paused = True
            self.musicPlayer.pause()
            self.bePaused.emit()
            # avoid kill after released

            self.pausedAt = self.now - self.startTime

    def toggle(self):
        if self.paused:
            self.start()
        else:
            self.pause()
        self.toogled.emit()

    def seek(self, time):
        oldPaused = self.paused
        self.pause()
        self.pausedAt = time
        self.update()
        if self.musicPlayer.isSeekable():
            self.musicPlayer.setPosition(int(time*2000)) # milisecond
        if not oldPaused:
            self.start()

    def capture(self):
        pic = QPixmap(self.width(), self.height())
        self.paintEvent(device=pic)
        pic.save("captures/cap-{}.png".format(time.strftime("%Y%m%d-%H_%M_%S")))

    def paintEvent(self, e=None, device=None) -> bool:
        if not device:
            painter = newPainter(self)
        else:
            painter = newPainter(device)
        painter.setRenderHints(newPainter.RenderHint.SmoothPixmapTransform | newPainter.RenderHint.Antialiasing, True)
        # painter.setBrush(QColor(0,0,0))
        # for i in self._debugRend: painter.drawRect(i)
        # painter.setBrush(QColor(0,0,0,0))
        # painter.setWindow(0, self.height(), self.width(), -self.height())
        painter.setWorldTransform(self.TRANSLATION)
        if not self.paused:
            self.now = time.perf_counter()
            # self._syncSong(int((self.now-self.startTime)* 1000))
        else:
            self.now = self.startTime+self.pausedAt
        painter.drawSong((self.now-self.startTime),
                                self.song)
        if self.mousePressedPos and self.mousePressAndMovedPos and self.drawr:
            painter.setBrush(QColor(86,114,240,160))
            painter.resetTransform()
            painter.drawRect(QRect(self.mousePressedPos,self.mousePressAndMovedPos))
        painter.drawStatus()
        painter.drawText(10,40,str(self.fpsPrint))
        self.fps += 1
        painter.end()

    def resizeEvent(self, a0: QResizeEvent) -> None:
        oldSize = self.size()
        self.sizeVar = a0.size()
        self.TRANSLATION.reset()
        self.TRANSLATION.rotate(180,Qt.Axis.XAxis)
        self.TRANSLATION.translate(0,-self.size().height())
        return super().resizeEvent(a0)

    def timerEvent(self, a0) -> None:
        if a0.timerId() == self.timer:
            self.update()
            # self.paintEvent()
            self.timeUpdate.emit(int(self.now-self.startTime))
        elif a0.timerId() == self.fpstimer:
            self.fpsPrint = self.fps*2
            self.fps=0
        return super().timerEvent(a0)
    
    def mousePressEvent(self, a0: QMouseEvent) -> None:
        
        self.mousePressedPos = a0.pos()
        self.selectionBefore =self.selectedObj.copy()
        return super().mousePressEvent(a0)
    
    def mouseMoveEvent(self, a0: QMouseEvent) -> None:
        self.mousePressAndMovedPos = a0.pos()
        if self.mousePressedPos and self.mousePressAndMovedPos:
            
            for rect, obj in self.objAndRects:
                # self._debugRend.append(rect) #DEBUG
                # if rect.intersected(QRect(self.mousePressedPos,self.mousePressAndMovedPos)).contains(rect): # 全部进入才算选择
                if rect.intersects(QRect(self.mousePressedPos,self.mousePressAndMovedPos)): # 有交集就算选择
                    if self.ShiftPressed and (obj in self.selectionBefore):
                        if obj in self.selectedObj:
                            self.selectedObj.remove(obj)
                    else:
                        self.selectedObj |= set([obj])
                elif (obj in self.selectedObj):
                    if self.ShiftPressed and obj in self.selectionBefore:
                        self.selectedObj |= set([obj])
                    else:
                        self.selectedObj.remove(obj)
                elif (obj in self.selectionBefore) and self.ShiftPressed:
                    self.selectedObj |= set([obj])
            self.update()
        # self.update()
        return super().mouseMoveEvent(a0)
    
    def mouseReleaseEvent(self, a0: QMouseEvent) -> None:
        self.mousePressedPos = None
        self.mousePressAndMovedPos = None
        self.selectionBefore = self.selectedObj.copy()
        self.update()
        return super().mouseReleaseEvent(a0)
    
    def keyPressEvent(self, a0: QKeyEvent) -> None:
        if a0.key() == Qt.Key.Key_Shift:
            self.ShiftPressed = True
        return super().keyPressEvent(a0)

    def keyReleaseEvent(self, a0: QKeyEvent) -> None:
        if a0.key() == Qt.Key.Key_Shift:
            self.ShiftPressed = False
        return super().keyReleaseEvent(a0)

    def loadSong(self, illustrationAddr=None, musicAddr=None, chartAddr=None,):
        if illustrationAddr or musicAddr:
            try:
                self.music = QMediaContent(QUrl(musicAddr))
                
            except FileNotFoundError:
                warn("Open music failed!")
                self.music = None
            try:
                self.illustration = QPixmap(illustrationAddr)
            except FileNotFoundError:
                warn("Open illustration failed")
        else:
            pass  # stay what they are

        if chartAddr:
            f = open(chartAddr)
            self.chart = officalChartLoader(f)
            f.close()
        self.song = Song(
                self.chart,
                self.illustration
        )
        self.startTime = time.perf_counter()
        self.now = self.startTime
        self.paused = True
        self.pausedAt = 0
        self.timer: Union[int, None] = None
        if self.music:
            self.musicPlayer.setMedia(self.music)
            self.musicPlayer.durationChanged.connect(self._durationReciver)
            self.musicPlayer.positionChanged.connect(self._positionReciver)
            # self.endTimeLoaded.emit(int(self.musicPlayer.duration()/1000))

    def _durationReciver(self,du):
        self.endTimeLoaded.emit(int(du/2000))
        self.rangeLoaded.emit(0,int(du/2000))
    
    def _positionReciver(self, pos):
        if pos >= self.musicPlayer.duration():
            self.pause()
    
    def _syncSong(self,nowTime):
        if abs(self.musicPlayer.position() - nowTime) >= 50:
            self.musicPlayer.setPosition(nowTime)
            print(abs(self.musicPlayer.position() - nowTime))
        

if __name__ == "__main__":
    app = QApplication([])
    win = QMainWindow()
    win.resize(800, 450)
    painter = newPainter()
    player = IntegratedPlayer(
        parent=win
    )
    player.loadSong(
        chartAddr="assets/Chart_IN_Error",
        musicAddr="assets/Introduction.mp3",
        illustrationAddr="./assets/IllustrationBlur.png",
    )
    player.resize(800, 450)
    player.start()
    win.show()
    app.exec()
