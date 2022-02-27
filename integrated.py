
import time
from typing import Union
from warnings import warn

from PyQt5.QtCore import QTimer, pyqtSignal
from PyQt5.QtGui import QImage, QResizeEvent
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget

import Properties as prop
from officalChartLoader import officalChartLoader
from Song import Song
from View import newPainter


class IntegratedPlayer(QWidget):

    timeUpdate = pyqtSignal(int)
    rangeLoaded = pyqtSignal(int, int) # TODO
    endTimeLoaded = pyqtSignal(int)# TODO

    def __init__(self, parent) -> None:

        super().__init__(parent)
        prop.screenWidth = 800
        prop.screenHeight = 450
        self.startTime = time.perf_counter()
        self.now = self.startTime
        self.paused = True
        self.pausedAt = 0
        self.timer: Union[int, None] = None

    def start(self):
        if self.paused:
            self.now = time.perf_counter()
            self.startTime = self.now-self.pausedAt
            # avoid duplicate defining
            self.timer = self.startTimer(10) if not self.timer else self.timer
            # self.musicPlayer.play()
            self.paused = False
            self.pausedAt = 0
    

    def pause(self):
        if not self.paused:
            self.paused = True
            # self.musicPlayer.pause()
            # avoid kill after released
            if self.timer:
                self.killTimer(self.timer)
                self.timer = None
            self.pausedAt = self.now - self.startTime

    def seek(self, time):
        oldPaused = self.paused
        self.pause()
        self.pausedAt = time
        self.update()
        if not oldPaused:
            self.start()
        # self.musicPlayer.seek(time)

    def paintEvent(self, e) -> bool:
        painter = newPainter(self)
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

    def loadSong(self, illustrationAddr, musicAddr, chartAddr,):
        if illustrationAddr or musicAddr:
            # try:
            #     self.music = pyglet.media.load(musicAddr)
            # except FileNotFoundError:
            #     warn("Open music failed!")
            #     self.music = None
            try:
                self.illustration = QImage(illustrationAddr)
            except FileNotFoundError:
                warn("Open illustration failed")
        else:
            self.music = None
            self.illustration = None
        f = open(chartAddr)
        self.song = Song(
            officalChartLoader(f),
            self.illustration)
        f.close()
        # self.musicPlayer = pyglet.media.Player()
        # if self.music:
        #     self.musicPlayer.queue(self.music)



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
