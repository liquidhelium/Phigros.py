

from Events import Events

class Line:

    def __init__(self, notesAbove, notesBelow, bpm: int, speedEvents: Events,
                 disappearEvents: Events, moveEvents: Events,
                 rotateEvents: Events):
        self.bpm = bpm
        self.notesAbove = notesAbove
        self.notesBelow = notesBelow
        self.speedEvents = speedEvents
        self.disappearEvents = disappearEvents
        self.moveEvents = moveEvents
        self.rotateEvents = rotateEvents

    
