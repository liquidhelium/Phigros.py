from bisect import bisect
from PyQt5.QtGui import QPixmap, QTransform
from PyQt5.QtCore import Qt

from .Line import Line
from .PhiTime import phiToSecond
from .HitAnimation import HitAnimation


class Note:

    def __init__(self, parent: Line, type, time, posX, holdTime, speed, floorPos, isBelow = False) -> None:
        trans = QTransform()
        trans.rotate(180, Qt.Axis.XAxis)
        self.texture_: list[QPixmap] = [
            None,
            QPixmap("./assets/tap.png").transformed(trans),
            QPixmap("./assets/drag.png").transformed(trans),
            QPixmap("./assets/hold.png").transformed(trans),
            QPixmap("./assets/flick.png").transformed(trans)
        ]
        self.parent = parent
        self.textureCache = None
        self.textureCacheRes = (0, 0)
        self.type = type
        self.time = float(time)
        self.posX = posX
        self.holdTime = holdTime
        self.speed = speed
        self.floorPos = floorPos
        self.hitAnimations: list[HitAnimation] = []
        self.hitRes = (0, 0)
        self.isBelow = isBelow

    def optmize(self, speedEv, bpm):
        self.FloorY = self.getFloorY()
        self.FloorX = self.getFloorX()
        if self.type == 3:
            spEvTail = speedEv.get(self.time+self.holdTime)
            self.tailY = phiToSecond(self.holdTime, bpm) * spEvTail[1]

    def genHit(self):
        if not self.type == 3:
            self.hitAnimations = []
            ang = self.parent.rotateEvents.getNoCache(self.time)
            pos = self.parent.moveEvents.getNoCache(self.time+1.0)
            trans = QTransform()
            trans.translate(pos[0], pos[1])
            trans.rotate(ang, Qt.Axis.ZAxis)
            self.hitAnimations = [HitAnimation(phiToSecond(
                self.time, self.parent.bpm), *trans.map(self.FloorX, 0))]
        else:
            self.hitAnimations = []
            for time in range(int(self.time), int(self.time+self.holdTime), 16):
                ang = self.parent.rotateEvents.getNoCache(time)
                pos = self.parent.moveEvents.getNoCache(time+1.0)
                trans = QTransform()
                trans.translate(pos[0], pos[1])
                trans.rotate(ang, Qt.Axis.ZAxis)
                self.hitAnimations.append(HitAnimation(phiToSecond(
                    float(time), self.parent.bpm), *trans.map(self.FloorX, 0)))

    def getFloorY(self):
        return self.floorPos

    def getFloorX(self):
        return (self.posX) / 18

    def getAnchor(self, img: QPixmap) -> tuple[float, float]:
        if self.type == 3:
            return img.width()/2, 5.0
        else:
            return img.width()/2, img.height()/2

    def __lt__(self, other):
        try:
            return self.floorPos < other
        except NotImplementedError:
            return self.floorPos < other.floorPos

    def __gt__(self, other):
        try:
            return self.floorPos > other
        except NotImplementedError:
            return self.floorPos > other.floorPos
    
    def __getstate__(self):
        # for pickle.
        state = self.__dict__.copy()
        unWant = [
            "texture_",
            # "parent",
            "textureCache",
            "textureCacheRes",
            "hitAnimations",
            "hitRes"
        ]
        for key in unWant:
            del state[key]
        return state
    
    def __setstate__(self,state:dict):
        trans = QTransform()
        trans.rotate(180, Qt.Axis.XAxis)
        self.texture_: list[QPixmap] = [
            None,
            QPixmap("./assets/tap.png").transformed(trans),
            QPixmap("./assets/drag.png").transformed(trans),
            QPixmap("./assets/hold.png").transformed(trans),
            QPixmap("./assets/flick.png").transformed(trans)
        ]
        self.textureCache = None
        self.textureCacheRes = (0, 0)
        
        self.hitAnimations: list[HitAnimation] = []
        self.hitRes = (0, 0)
        for key, value in state.items():
            self.__setattr__(key,value)

class Notes(list[Note]):

    def __init__(self, parent: Line, *arg) -> None:
        self.parent = parent
        super().__init__(*arg)

    def getNearNotes(self, time):
        yline = self.parent.getFloorAtTime(time)
        max = bisect(self, yline + 5)
        min = bisect(self, yline - 5)
        return self[min:max]
    
    def __getstate__(self):
        state = self.__dict__.copy()
        # del state["parent"]
        return state
