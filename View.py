from pyglet.gl import *
from pyglet.image import ImageData

import Properties as prop

def draw(img: ImageData, x, y, ang):
    glTranslatef(x*800,y*450,0.0)
    glRotatef(ang,0.0,0.0,1.0)
    img.blit(-img.width/2,-img.height/2)
    glTranslatef(-x*800,-y*450,0.0)
    glRotatef(-ang,0.0,0.0,1.0)
    

class Rotation:
    def __init__(self, ang):
        self.ang = ang
    
    def __enter__(self):
        glRotatef(self.ang,0.0,0.0,1.0)
    
    def __exit__(self,type,value,trace):
        glRotatef(-self.ang,0.0,0.0,1.0)


class TranslationPhi:
    def __init__(self, phiX, phiY):
        self.X = phiX * prop.screenWidth
        self.Y = phiY * prop.screenHeight
    
    def __enter__(self):
        glTranslatef(self.X, self.Y, 0.0)
    
    def __exit__(self,type,value,trace):
        glTranslatef(-self.X, -self.Y, 0.0)
    
