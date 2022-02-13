import pyglet
from pyglet.gl import *


# Pyglet Window stuff ---------------------------------------------------------
batch = pyglet.graphics.Batch()  # holds all graphics
config = Config(sample_buffers=1, samples=4,depth_size=16, double_buffer=True, mouse_visible=False)
window = pyglet.window.Window(fullscreen=False, config=config)

glClearColor(  0, 100,   0, 255)  # background color
glEnable(GL_LINE_SMOOTH)
glHint(GL_LINE_SMOOTH_HINT, GL_DONT_CARE)
glEnable(GL_BLEND)                                  # transparency
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)   # transparency

play_text = pyglet.text.Label("Play", font_name="Arial", font_size=32, x=240, y=140, anchor_x='center', anchor_y='center', color=(255,0,255,100), batch=batch,group=None)
text_box = pyglet.sprite.Sprite(pyglet.image.load('assets/line.png'),240-150,160-25, batch=batch,group=None)

@window.event
def draw(dt):
    window.clear()
    batch.draw()


if __name__ == "__main__":
    pyglet.clock.schedule_interval(draw, 1.0/60)
    pyglet.app.run()