from pyglet.image import AbstractImage
from Chart import Chart
import pyglet.sprite

class Song:
    def __init__(self, chart: Chart, music = None, illustration: AbstractImage = None):
        self.chart=chart
        self.music=music
        self.illustration=illustration
    
    async def render(self, time):
        try:
            sprite = pyglet.sprite.Sprite(self.illustration) 

            H_ratio = max(sprite.height, 450)/min(sprite.height, 450) 
            W_ratio = max(sprite.width, 800)/min(sprite.width, 800) 

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