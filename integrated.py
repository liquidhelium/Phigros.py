
import typing
from warnings import warn
from PyQt5.QtWidgets import QOpenGLWidget, QWidget, QMainWindow, QApplication
from PyQt5 import QtCore
from PyQt5.QtGui import QImage
from PyQt5.QtCore import QTimer

from Song import Song
from View import newPainter
from getSize import getHeight, getWidth
from officalChartLoader import officalChartLoader
import Properties as prop

import pyglet
from pyglet import clock
import time
from OpenGL.GL import *
from threading import Timer

class IntergratedPlayerd(pyglet.window.Window):
    def __init__(self, chartAddr, musicAddr = None, illustrationAddr = None,
                    width=800, height = 450,*w,**kw
                    ):
        super().__init__(width,height,*w,**kw)
        glEnable(GL_LINE_SMOOTH)
        glHint(GL_LINE_SMOOTH_HINT, GL_DONT_CARE)
        glEnable(GL_BLEND)  # transparency
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)  # transparency
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        # 谱面
        prop.screenWidth = width
        prop.screenHeight = height
        if illustrationAddr and musicAddr:
            try:
                self.music = pyglet.media.load(musicAddr)
            except FileNotFoundError:
                warn("Open music failed!")
                self.music = None
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
        self.musicPlayer = pyglet.media.Player()
        if self.music:
            self.musicPlayer.queue(self.music)
        self.startTime = 0
        self.paused = False
        self.pausedAt = 0
        self.fpsDisplay = pyglet.window.FPSDisplay(self)
        self.fpsDisplay.update_period = 1
    
    def start(self):
        self.now = time.perf_counter()
        self.startTime = self.now - self.pausedAt
        self.musicPlayer.play()
        self.paused = False
        self.pausedAt = 0
    
    def on_draw(self):
        self.clear()
        
        self.fpsDisplay.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        if button == 4:
             self.start() if self.paused else self.pause()
        

    def pause(self):
        self.paused = True
        self.musicPlayer.pause()
        self.pausedAt = self.now - self.startTime

    def seek(self, time):
        self.startTime -= time
        self.musicPlayer.seek(time)
    
    def _syncSong(self):
        if abs(self.musicPlayer.time - self.now + self.startTime) > 0.1:
            self.musicPlayer.seek(self.now - self.startTime)

class IntergratedPlayer(QOpenGLWidget):
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


    def paintGL(self) -> bool:
        glLoadIdentity()
        glClear(GL_COLOR_BUFFER_BIT)
        glEnable(GL_LINE_SMOOTH)
        glHint(GL_LINE_SMOOTH_HINT, GL_DONT_CARE)
        glEnable(GL_BLEND)  # transparency
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)  # transparency
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        self.painter.begin(self)
        self.painter.setCompositionMode(self.painter.CompositionMode.CompositionMode_SourceOver)
        if not self.paused:
            self.now = time.perf_counter()
            # self._syncSong()
        try:
            self.song.render((self.now-self.startTime),self.painter).send(None)
            print("rend")
        except StopIteration:
            pass
        self.painter.end()
        


    def initializeGL(self) -> None:
        glEnable(GL_LINE_SMOOTH)
        glHint(GL_LINE_SMOOTH_HINT, GL_DONT_CARE)
        glEnable(GL_BLEND)  # transparency
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)  # transparency
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    
    def resizeGL(self, w: int, h: int) -> None:
        prop.screenWidth = w
        prop.screenHeight = h
        return super().resizeGL(w, h)
    

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
    timer.setInterval(int(100/6))
    timer.timeout.connect(player.update)
    timer.start()
    win.show()
    app.exec()
    # Timer(5,player.pause).start()
    # Timer(10,player.start).start()
    # pyglet.app.run()
