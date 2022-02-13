from pyglet.image import AbstractImage
from Chart import Chart

class Song:
    def __init__(self, chart: Chart, music = None, illustration: AbstractImage = None):
        self.chart=chart
        self.music=music
        self.illustration=illustration
    

    def render(self, time):
        self.illustration.blit(0,0)
        self.chart.render(time)