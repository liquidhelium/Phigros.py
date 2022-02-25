from pyglet.image import ImageData, create, SolidColorImagePattern
from Chart import Chart
from getSize import *

class Song:
    cover = create(1000, 1000, 
                    SolidColorImagePattern((0,0,0,128))).get_texture()
    def __init__(self, chart: Chart, illustration: ImageData = None):
        self.chart=chart
        self.illustration=illustration
    
    async def render(self, RTime):
        try:
            if self.illustration:
                texture = self.illustration.get_texture()
                texture.height = getHeight(450)
                texture.width = getWidth(800)
                texture.blit(0,0)
                Song.cover.height = texture.height
                Song.cover.width = texture.width
                Song.cover.blit(0,0)
            self.chart.render(RTime).send(None)
        except StopIteration: pass
