from pyglet.image import ImageData
from Chart import Chart
import Properties as prop

class Song:
    def __init__(self, chart: Chart, music = None, illustration: ImageData = None):
        self.chart=chart
        self.music=music
        self.illustration=illustration
    
    async def render(self, time):
        try:

            H_ratio = max(self.illustration.height, prop.screenHeight)/\
                    min(self.illustration.height, prop.screenHeight) 
            W_ratio = max(self.illustration.width, prop.screenWidth)/\
                    min(self.illustration.width, prop.screenWidth) 

            self.illustration.scale = max(H_ratio, W_ratio)
            texture = self.illustration.get_texture()
            texture.height = 450
            texture.width = 800
            texture.blit(0,0)
            self.chart.render(time).send(None)
        except StopIteration: pass

    def play(self,player,time):
        player.queue(self.music)
        player.play()
        player.seek(time)