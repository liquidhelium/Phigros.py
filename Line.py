import pyglet.image

class Line:
    texture = pyglet.image.load("assets/line.png")

    def __init__(self, notesAbove, notesBelow, 
                speedEvents, disappearEvents, moveEvents, rotateEvents):
        self.notesAbove = notesAbove
        self.notesBelow = notesBelow
        self.speedEvents = speedEvents
        self.disappearEvents = disappearEvents
        self.moveEvents = moveEvents
        self.rotateEvents = rotateEvents


    def render(time):pass
