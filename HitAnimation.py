from math import floor
import pyglet
from pyglet.image import ImageData



def optimizeTexture(texture: ImageData, segment):
    if texture.height % segment != 0:
        raise ValueError
    raw = bytearray(texture.get_data("BGRA"))
    length = texture.width * segment * len(texture.format)
    last = 0 
    for i in range(texture.height // segment):
        sliced = raw[last:last + length]
        for pos, value in enumerate(sliced):
            if (pos+1) % 4 == 0 and value != 0:
                sliced[pos] = int(value * (i/(texture.height // segment)))
                pass
        yield pyglet.image.ImageData(texture.width, segment, texture.format, 
                                bytes(sliced)).get_texture()
        last = last + length



rawTexture: ImageData = pyglet.image.load("assets\\perfect.png")
print(rawTexture.format)
        
textures = list(optimizeTexture(rawTexture, 256))
def getHit(realTime):
    if realTime <= 0 or realTime > 0.5:
        return
    return textures[floor(realTime * 60)]

