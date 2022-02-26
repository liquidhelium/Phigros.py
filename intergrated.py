
import time
from warnings import warn

from OpenGL.GL import *
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QResizeEvent
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget

import Properties as prop
from officalChartLoader import officalChartLoader
from Song import Song
from View import newPainter


class IntergratedPlayer(QWidget):
    def __init__(self, painter: newPainter, illustrationAddr, musicAddr, chartAddr, 
            parent) -> None:
        
        super().__init__(parent)
        self.painter = painter
        prop.screenWidth=800
        prop.screenHeight = 450
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
        f= open(chartAddr)
        self.song = Song(
            officalChartLoader(f),
            self.illustration)
        f.close()
        # self.musicPlayer = pyglet.media.Player()
        # if self.music:
        #     self.musicPlayer.queue(self.music)
        self.startTime = time.perf_counter()
        self.now = self.startTime
        self.paused = False
        self.pausedAt = 0


    def paintEvent(self,e) -> bool:
        # glLoadIdentity()
        # glClear(GL_COLOR_BUFFER_BIT)
        # glEnable(GL_LINE_SMOOTH)
        # glHint(GL_LINE_SMOOTH_HINT, GL_DONT_CARE)
        # glEnable(GL_BLEND)  # transparency
        # glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)  # transparency
        # glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        self.painter.begin(self)
        self.painter.setCompositionMode(self.painter.CompositionMode.CompositionMode_SourceOver)
        self.painter.setWindow(0,self.height(),self.width(),-self.height())
        if not self.paused:
            self.now = time.perf_counter()
            # self._syncSong()
        try:
            self.song.render((self.now-self.startTime),self.painter).send(None)
        except StopIteration:
            pass
        self.painter.end()
        


    def resizeEvent(self, a0: QResizeEvent) -> None:
        prop.screenWidth = a0.size().width()
        prop.screenHeight = a0.size().height()
        return super().resizeEvent(a0)
    

    def start(self):
        self.now = time.perf_counter()
        self.startTime = self.now - self.pausedAt
        # self.musicPlayer.play()
        self.paused = False
        self.pausedAt = 0

if __name__ == "__main__":
    app = QApplication([])
    win = QMainWindow()
    win.resize(800,450)
    painter = newPainter()
    player = IntergratedPlayer( 
        painter= painter,
        chartAddr="assets/Chart_IN_Error", 
        musicAddr="assets/Introduction.mp3",
        illustrationAddr = "./assets/IllustrationBlur.png",
        parent=win
        )
    player.resize(800,450)
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
