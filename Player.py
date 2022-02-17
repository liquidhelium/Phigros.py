from Song import Song
from officalChartLoader import officalChartLoader
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
        # 谱面
        self.song = song
        self.second = 0
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
                pass

    def tick(self, dt):
        self.second += dt


# with open("assets/Introduction_chart.json") as f:
with open("assets/Chart_IN_Error") as f:
    chart = officalChartLoader(f)
    song = Song(
        chart,
        None,  # pyglet.media.load("assets/Introduction.mp3"),
        pyglet.image.load("assets/illustrationBlur.png"))
    win = MyPlayer(song, 800, 450)
    prop.screenHeight, prop.screenWidth = (450, 800)
    # player = pyglet.media.Player()
    # song.play(player,win.second+0.5)
    clock.schedule_interval(win.tick, 1 / 60)
pyglet.app.run()
