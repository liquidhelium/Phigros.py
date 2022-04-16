from math import cos, floor, pi, sin
import random
from PyQt5.QtGui import QImage
from PyQt5.QtCore import QRect, QPoint
import time



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
        
textures = list(optimizeTexture(rawTexture, 256))
def getHit(realTime):
    if realTime < 0 or realTime >= 0.5:
        return
    return textures[floor(realTime * 60)]

class HitAnimation:
    def __init__(self,startTime,x,y) -> None:
        self.startTime = startTime
        self.NowTime = -1
        self.x = x
        self.y = y
        self.randparticales = []
        for _ in range(7):
            self.randparticales.append((random.uniform(0,2*pi),random.uniform(0.7,1))) # 角度, 距离

    def getTexture(self):
        hit = getHit(self.NowTime-self.startTime)
        # if not hit:
        #     del self
        return hit

    def genParticles(self,maxDist=100) -> list[QPoint]:
        realTime = self.NowTime-self.startTime
        if realTime < 0 or realTime >= 0.5:
            return
        percent = -(realTime*2)**2 + (realTime*2)*2
        return [QPoint(int((percent*maxDist*j)*cos(i)+self.x),int((percent*maxDist*j)*sin(i)+self.y)) for i,j in self.randparticales]

    def updateTime(self, now):
        self.NowTime = now

    def getPercent(self):
        return (self.NowTime-self.startTime)/0.5
        
