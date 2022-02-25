
from warnings import warn
from Song import Song
from officalChartLoader import officalChartLoader
import Properties as prop

import pyglet
from pyglet import clock
import time
from pyglet.gl import *
from threading import Timer

class IntergratedPlayer(pyglet.window.Window):
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
                self.illustration = pyglet.image.load(illustrationAddr)
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
        if not self.paused:
            self.now = time.perf_counter()
            self._syncSong()
        try:
            self.song.render((self.now-self.startTime)).send(None)
        except StopIteration:
            pass
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

if __name__ == "__main__":
    player = IntergratedPlayer("assets/Introduction_chart.json", "assets/Introduction.mp3",
         illustrationAddr = "./assets/IllustrationBlur.png", caption ="phi")
    player.start()
    player.seek(14)
    clock.schedule_interval(clock.tick,1/100)
    # Timer(5,player.pause).start()
    # Timer(10,player.start).start()
    pyglet.app.run()
