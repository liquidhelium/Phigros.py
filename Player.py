from Song import Song
from officalChartLoader import officalChartLoader
import pyglet
from pyglet import clock
from pyglet.gl import *
class MyPlayer(pyglet.window.Window):
    def __init__(self, song: Song, *w):
        super(MyPlayer,self).__init__(*w)
        glEnable(GL_LINE_SMOOTH)
        glHint(GL_LINE_SMOOTH_HINT, GL_DONT_CARE)
        glEnable(GL_BLEND)                                  # transparency
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)   # transparency
        #谱面
        self.song = song
        self.second = 85
        self.need_draw=[
                self.song,
                            ]
    def on_draw(self):
        self.clear()
        for draw_object in self.need_draw:
            try:
                draw_object.render(time = (self.second / (60/138) * 32)).send(None)
            except StopIteration:
                pass
    def tick(self,dt):
        self.second+=dt

with open("assets/Introduction_chart.json") as f:
    chart = officalChartLoader(f)
    song = Song(chart,pyglet.media.load("assets/Introduction.mp3"),pyglet.image.load("assets/illustrationBlur.png"))
    win = MyPlayer(song, 800, 450)
    player = pyglet.media.Player()
    song.play(player, win.second+2.5)
    clock.schedule_interval(win.tick,1/60)
pyglet.app.run()
