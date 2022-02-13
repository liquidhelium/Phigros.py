from pyglet.gl import *
from pyglet.image import AbstractImage
import pyglet

def draw(img: AbstractImage, x, y, ang):
    #glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(x*600,y*600,0.0)
    glRotatef(ang,0.0,0.0,1.0)
    img.blit(-img.width/2,-img.height/2)


