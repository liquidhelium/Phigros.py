from Song import Song
from officalChartLoader import officalChartLoader, optmize
import pyglet
from pyglet import clock
from pyglet.gl import *
import Properties as prop


class MyPlayer(pyglet.window.Window):

    def __init__(self, song: Song, *w):
        super(MyPlayer, self).__init__(*w)
        glEnable(GL_LINE_SMOOTH)
        glHint(GL_LINE_SMOOTH_HINT, GL_DONT_CARE)
        glEnable(GL_BLEND)  # transparency
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)  # transparency
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        # 谱面
        self.song = song
        self.second = 80
        self.need_draw = [
            self.song,
        ]

    def on_draw(self):
        self.clear()
        for draw_object in self.need_draw:
            try:
                time = (self.second / (60 / 209) * 32)
                draw_object.render(time).send(None)
            except StopIteration:
                prop.fps += 1

    def tick(self, dt):
        self.second += dt

    def printFPS(self, dt):
        print(prop.fps)
        prop.fps = 0


# with open("assets/Introduction_chart.json") as f:
with open("assets/Chart_IN_Error") as f:
    chart = officalChartLoader(f)
    song = Song(
        chart,
         pyglet.media.load("assets/Introduction.mp3"),
        pyglet.image.load("assets/illustrationBlur.png"))
    win = MyPlayer(song, 800, 450)
    prop.screenHeight, prop.screenWidth = (450, 800)
    optmize(song.chart)
    prop.fps = 0
    player = pyglet.media.Player()
    song.play(player,win.second+0.5)
    clock.schedule_interval(win.tick, 1 / 200)
    clock.schedule_interval(win.printFPS, 1)
pyglet.app.run()
