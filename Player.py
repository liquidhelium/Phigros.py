from Song import Song
from officalChartLoader import officalChartLoader, optimize
import pyglet
from pyglet import clock
from pyglet.gl import *
import Properties as prop


class SongPlayer(pyglet.window.Window):

    def __init__(self, song: Song,player, *w, **kw):
        super(SongPlayer, self).__init__(*w,**kw)
        glEnable(GL_LINE_SMOOTH)
        glHint(GL_LINE_SMOOTH_HINT, GL_DONT_CARE)
        glEnable(GL_BLEND)  # transparency
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)  # transparency
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        # 谱面
        self.song = song
        self.player = player
        self.second = 0
        self.fpsDisplay = pyglet.window.FPSDisplay(self)
        self.fpsDisplay.update_period=1
        self.need_draw = [
            self.song,
        ]

    def on_draw(self):
        self.clear()
        try:
            self.song.render(self.second).send(None)
        except StopIteration:
            pass
        self.fpsDisplay.draw()

    def tick(self, dt):
        self.second += dt

    
    def syncSong(self, dt):
        if abs(self.player.time - self.second) > 0.1:
            self.player.seek(self.second)


# with open("assets/Introduction_chart.json") as f:
with open("assets/Chart_IN_Error") as f:
    chart = officalChartLoader(f)
    song = Song(
        chart,
        pyglet.image.load("assets/illustrationBlur.png"))
    player = pyglet.media.Player()
    win = SongPlayer(song, player, 800, 450,caption ="phi",style = pyglet.window.Window.WINDOW_STYLE_BORDERLESS)
    prop.screenHeight, prop.screenWidth = (450, 800)
    optimize(song.chart)
    
    song.play(player,win.second)
    clock.schedule_interval(win.tick, 0.005)
    #clock.schedule_interval(win.syncSong, 10)
    
pyglet.app.run()