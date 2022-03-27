
import time
from typing import Union
from warnings import warn

from PyQt5.QtCore import pyqtSignal, QUrl
from PyQt5.QtGui import QImage, QResizeEvent, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent

from officalChartLoader import officalChartLoader
from Song import Song
from View import newPainter



class IntegratedPlayer(QWidget):

    timeUpdate = pyqtSignal(int)
    rangeLoaded = pyqtSignal(int, int)
    endTimeLoaded = pyqtSignal(int)
    toogled = pyqtSignal() 
    bePaused = pyqtSignal()
    bePlayed = pyqtSignal()

    def __init__(self, parent) -> None:

        super().__init__(parent)
        self.startTime = time.perf_counter()
        self.now = self.startTime
        self.paused = False
        self.pausedAt = 0
        self.fps = 0
        self.fpstimer = self.startTimer(1000)
        self.timer: Union[int, None] = None
        self.musicPlayer = QMediaPlayer(self)
        self.pause()


    def start(self):
        if self.paused:
            # avoid duplicate defining
            self.timer = self.startTimer(6) if not self.timer else self.timer
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
            self.musicPlayer.setPosition(int(time*1000)) # milisecond
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
        painter.setWindow(0, self.height(), self.width(), -self.height())
        if not self.paused:
            self.now = time.perf_counter()
            # self._syncSong(int((self.now-self.startTime)* 1000))
        else:
            self.now = self.startTime+self.pausedAt
        painter.drawSong((self.now-self.startTime),
                                self.song)
        self.fps += 1
        painter.end()

    def resizeEvent(self, a0: QResizeEvent) -> None:
        self.size = a0.size()
        return super().resizeEvent(a0)

    def timerEvent(self, a0) -> None:
        if a0.timerId() == self.timer:
            self.update()
            # self.paintEvent()
            self.timeUpdate.emit(int(self.now-self.startTime))
        elif a0.timerId() == self.fpstimer:
            print(self.fps)
            self.fps=0
        return super().timerEvent(a0)

    def loadSong(self, illustrationAddr=None, musicAddr=None, chartAddr=None,):
        if illustrationAddr or musicAddr:
            try:
                self.music = QMediaContent(QUrl(musicAddr))
                
            except FileNotFoundError:
                warn("Open music failed!")
                self.music = None
            try:
                self.illustration = QImage(illustrationAddr)
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
        self.endTimeLoaded.emit(int(du/1000))
        self.rangeLoaded.emit(0,int(du/1000))
    
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
    # Timer(5,player.pause).start()
    # Timer(10,player.start).start()
    # pyglet.app.run()
