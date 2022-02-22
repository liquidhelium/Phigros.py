from email.mime import image
from math import floor
import pyglet
from pyglet.image import ImageData



def cutTexture(texture: ImageData, segment):
    if texture.height % segment != 0:
        raise ValueError
    raw = texture.get_data("byte")
    length = texture.width * segment * len(texture.format)
    last = 0 
    for i in range(texture.height // segment):
        yield pyglet.image.ImageData(texture.width, segment, texture.format, 
                                bytes(raw[last:last + length])).get_texture()
        last = last + length



rawTexture: ImageData = pyglet.image.load("assets\\perfect.png")

textures = list(cutTexture(rawTexture, 256))
def getHit(realTime):
    if realTime <= 0 or realTime > 0.5:
        return
    return textures[floor(realTime * 60)]

