from math import floor
from PyQt5.QtGui import QImage
from PyQt5.QtCore import QRect



def optimizeTexture(texture: QImage, segment: int):
    if texture.height() % segment != 0:
        raise ValueError
    for i in range(texture.height() // segment):
        sliced = texture.copy(QRect(0,i*segment,texture.width(),segment))
        # for pos, value in enumerate(sliced):
        #     if (pos+1) % 4 == 0 and value != 0:
        #         sliced[pos] = int(value * (i/(texture.height() // segment)))
        #         pass
        yield sliced



rawTexture= QImage("assets\\perfect.png")
        
textures = list(reversed(list(optimizeTexture(rawTexture, 256))))
def getHit(realTime):
    if realTime <= 0 or realTime > 0.5:
        return
    return textures[floor(realTime * 60)]

