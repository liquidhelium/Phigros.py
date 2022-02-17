#-*- coding:utf-8 -*-
import pyglet.image
from pyglet import clock
from pyglet.gl import *

image = pyglet.image.load("assets\\line.png")


def draw_rect(x, y, z, width, height, ang):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(x, y, 0.0)
    glRotatef(ang, 0.0, 0.0, 1.0)
    image.blit(-image.width / 2, 0)


class Button():
    x = y = z = 0
    width = height = 10.0
    ang = 0

    def draw(self):
        draw_rect(self.x, self.y, self.z, self.width, self.height, self.ang)


class MyWindow(pyglet.window.Window):

    def __init__(self, *w):
        super(MyWindow, self).__init__(*w)
        #按钮
        self.button = Button()
        self.button.x = 300
        self.button.y = 300
        self.button.z = 0
        self.button.width = self.width / 2
        self.button.height = self.height / 2
        self.button.ang = 0

        self.need_draw = [
            self.button,
        ]

    def on_draw(self):
        self.clear()
        for draw_object in self.need_draw:
            draw_object.draw()

    def value_change(self, dt):
        self.button.ang += dt * 10


if __name__ == "__main__":
    wn = MyWindow(600, 600)
    clock.schedule_interval(wn.value_change, 1 / 60)
pyglet.app.run()
