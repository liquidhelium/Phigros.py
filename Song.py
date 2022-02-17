from pyglet.image import AbstractImage
from Chart import Chart
import pyglet.sprite
import Properties as prop

class Song:
    def __init__(self, chart: Chart, music = None, illustration: AbstractImage = None):
        self.chart=chart
        self.music=music
        self.illustration=illustration
    
    async def render(self, time):
        try:
            sprite = pyglet.sprite.Sprite(self.illustration) 

            H_ratio = max(sprite.height, prop.screenHeight)/\
                    min(sprite.height, prop.screenHeight) 
            W_ratio = max(sprite.width, prop.screenWidth)/\
                    min(sprite.width, prop.screenWidth) 

            sprite.scale = max(H_ratio, W_ratio)
            sprite.x = 0
            sprite.y = 0
            sprite.draw()
            self.chart.render(time).send(None)
        except StopIteration: pass

    def play(self,player,time):
        player.queue(self.music)
        player.play()
        player.seek(time)