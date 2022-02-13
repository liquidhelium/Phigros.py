import json
from io import TextIOWrapper

from Chart import Chart
from Events import Event, Events
from Line import Line


def makeEvent(obj):
    return Event(**obj)

def makeEvents(obj):
    return Events([makeEvent(event) for event in obj])

def makeLine(obj):
    return Line(None, None, # Not ready yet
                None, # makeEvents(obj["speedEvents"]),
                makeEvents(obj["judgeLineDisappearEvents"]),
                makeEvents(obj["judgeLineMoveEvents"]),
                makeEvents(obj["judgeLineRotateEvents"])
                )

def officalChartLoader(file: TextIOWrapper):
    filejson = json.load(file)
    ver = filejson['formatVersion']
    offset = filejson['offset']
    notesCount = filejson['numOfNotes']
    lines = [makeLine(line) for line in filejson["judgeLineList"]]
    return Chart(ver, offset, notesCount, lines)
