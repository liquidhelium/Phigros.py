from functools import reduce
import json
from io import TextIOWrapper

from Chart import Chart
from Events import Event, SpeedEvent, OneNumEvent,Events
from Line import Line
from Notes import Note, Notes
from PhiTime import phiToSecond


def makeEvents(obj):
    return Events([Event(**event) for event in obj])



def realFloorSetterMaker(bpm):
    def setRealFloor(obj1,obj2: SpeedEvent) -> float:
        if isinstance(obj1,float):
            obj2.realFloor = obj1
        else:
            obj2.realFloor = phiToSecond(obj1.endTime,bpm)*obj1.value
        return obj2.realFloor
    return setRealFloor

def makeSpeedEvents(obj,bpm):
    evList =[SpeedEvent(**event) for event in obj]
    reduce(realFloorSetterMaker(bpm),evList)
    return Events(evList)

def makeOneNumEvents(obj):
    return Events([OneNumEvent(**event) for event in obj])

def makeNote(obj):
    return Note(obj["type"],obj["time"],obj["positionX"],obj["holdTime"], 
                    obj["speed"], obj["floorPosition"])

def makeLine(obj):
    bpm = obj["bpm"]
    return Line(Notes([makeNote(note) for note in obj["notesAbove"]]),
                Notes([makeNote(note) for note in obj["notesBelow"]]), 
                bpm,
                makeSpeedEvents(obj["speedEvents"],bpm),
                makeOneNumEvents(obj["judgeLineDisappearEvents"]),
                makeEvents(obj["judgeLineMoveEvents"]),
                makeOneNumEvents(obj["judgeLineRotateEvents"])
                )

def officalChartLoader(file: TextIOWrapper):
    filejson = json.load(file)
    ver = filejson['formatVersion']
    offset = filejson['offset']
    notesCount = filejson['numOfNotes']
    lines = [makeLine(line) for line in filejson["judgeLineList"]]
    return Chart(ver, offset, notesCount, lines)
