import json
from functools import reduce
from io import TextIOWrapper

from .Chart import Chart
from .Events import Event, Events, OneNumEvent, SpeedEvent
from .Line import Line
from .Notes import Note, Notes
from .PhiTime import phiToSecond


def makeEvents(obj):
    return Events([Event(**event) for event in obj])


def realFloorSetterMaker(bpm):

    def setRealFloor(obj1, obj2: SpeedEvent) -> float:
        if isinstance(obj1, float):
            obj2.realFloor = obj1
        else:
            obj2.realFloor = phiToSecond(obj1.endTime - obj1.startTime,
                                         bpm) * obj1.value
        return obj2.realFloor + phiToSecond(obj2.endTime - obj2.startTime,
                                            bpm) * obj2.value

    return setRealFloor


def makeSpeedEvents(obj, bpm):
    evList = [SpeedEvent(**event) for event in obj]
    reduce(realFloorSetterMaker(bpm), evList)
    return Events(evList)


def makeOneNumEvents(obj):
    return Events([OneNumEvent(**event) for event in obj])


def makeNote(obj, parent, below = False):
    return Note(parent, obj["type"], obj["time"], obj["positionX"], obj["holdTime"],
                obj["speed"], obj["floorPosition"],below)


def makeLine(obj):
    bpm = obj["bpm"]
    line = Line(Notes(None),
                Notes(None), bpm,
                makeSpeedEvents(obj["speedEvents"], bpm),
                makeOneNumEvents(obj["judgeLineDisappearEvents"]),
                makeEvents(obj["judgeLineMoveEvents"]),
                makeOneNumEvents(obj["judgeLineRotateEvents"]))
    line.notesAbove = Notes(line, [makeNote(note, line)
                            for note in obj["notesAbove"]])
    line.notesBelow = Notes(line, [makeNote(note, line, True)
                            for note in obj["notesBelow"]])
    return line


def officalChartLoader(file: TextIOWrapper):
    filejson = json.load(file)
    ver = filejson['formatVersion']
    offset = filejson['offset']
    notesCount = filejson['numOfNotes']
    lines = [makeLine(line) for line in filejson["judgeLineList"]]
    chart = Chart(ver, offset, notesCount, lines)
    optimize(chart)
    return chart


def optimize(chart):
    lines = chart.lines
    for line in lines:
        for note in line.notesAbove:
            note.optmize(line.speedEvents, line.bpm)
        for note in line.notesBelow:
            note.optmize(line.speedEvents, line.bpm)
