
import time
from typing import Union
from warnings import warn

from PyQt5.QtCore import QTimer, pyqtSignal, QUrl
from PyQt5.QtGui import QImage, QResizeEvent, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent

import Properties as prop
from officalChartLoader import officalChartLoader
from Song import Song
from View import newPainter


class IntegratedPlayer(QWidget):

    timeUpdate = pyqtSignal(int)
    rangeLoaded = pyqtSignal(int, int)  # TODO
    endTimeLoaded = pyqtSignal(int)  # TODO

    def __init__(self, parent) -> None:

        super().__init__(parent)
        prop.screenWidth = 800
        prop.screenHeight = 450
        self.startTime = time.perf_counter()
        self.now = self.startTime
        self.paused = True
        self.pausedAt = 0
        self.timer: Union[int, None] = None
        self.musicPlayer = QMediaPlayer(self)


    def start(self):
        if self.paused:
            # avoid duplicate defining
            self.timer = self.startTimer(10) if not self.timer else self.timer
            self.now = time.perf_counter()
            self.startTime = self.now-self.pausedAt
            self.musicPlayer.play()
            self.paused = False
            self.pausedAt = 0

    def pause(self):
        if not self.paused:
            if self.timer:
                self.killTimer(self.timer)
                self.timer = None
            self.paused = True
            self.musicPlayer.pause()
            # avoid kill after released

            self.pausedAt = self.now - self.startTime

    def toggle(self):
        if self.paused:
            self.start()
        else:
            self.pause()

    def seek(self, time):
        oldPaused = self.paused
        self.pause()
        self.pausedAt = time
        self.update()
        if self.musicPlayer.isSeekable():
            self.musicPlayer.setPosition(time*1000) # milisecond
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
        painter.setCompositionMode(
            painter.CompositionMode.CompositionMode_SourceOver)
        painter.setWindow(0, self.height(), self.width(), -self.height())
        if not self.paused:
            self.now = time.perf_counter()
            # self._syncSong()
        else:
            self.now = self.startTime+self.pausedAt
        try:
            self.song.render((self.now-self.startTime),
                             painter).send(None)
        except StopIteration:
            pass
        painter.end()

    def resizeEvent(self, a0: QResizeEvent) -> None:
        prop.screenWidth = a0.size().width()
        prop.screenHeight = a0.size().height()
        return super().resizeEvent(a0)

    def timerEvent(self, a0) -> None:
        self.update()
        self.timeUpdate.emit(int(self.now-self.startTime))
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
    timer = QTimer()
    timer.setInterval(int(10))
    timer.timeout.connect(player.update)
    timer.start()
    win.show()
    app.exec()
    # Timer(5,player.pause).start()
    # Timer(10,player.start).start()
    # pyglet.app.run()
