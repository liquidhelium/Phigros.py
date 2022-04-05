from bisect import bisect


def interpolate(x1, y1, x2, y2, x):
    "返回线性插值."
    try:
        return y1 + (x - x1) * ((y2 - y1) / (x2 - x1))
    except ZeroDivisionError:
        return y1


class Event:
    "基础的事件."

    def __init__(self, startTime, endTime, start=0, end=0, start2=0, end2=0):
        self.startTime = startTime
        self.endTime = endTime
        self.start = start
        self.end = end
        self.start2 = start2
        self.end2 = end2

    def __lt__(self, other):  # a < b
        return other.startTime >= self.endTime

    def __contains__(self, time):  # a in b
        return self.startTime <= time and self.endTime > time

    def get(self, time):
        return (interpolate(self.startTime, self.start, self.endTime, self.end,
                            time),
                interpolate(self.startTime, self.start2, self.endTime,
                            self.end2, time))


class SpeedEvent(Event):

    def __init__(self, startTime, endTime, floorPosition, value, realFloor=0):
        super().__init__(startTime, endTime)
        self.floorPos = floorPosition
        self.value = value
        self.realFloor = realFloor

    def get(self,time):
        return self.floorPos, self.value, self.startTime


class OneNumEvent(Event):

    def get(self, time):
        return interpolate(self.startTime, self.start, self.endTime, self.end,
                           time)


class Events(list[Event]):

    def __init__(self, *pra) -> None:
        super().__init__(*pra)
        self.cache = 0
        self.lastTime = 0

    def get(self, time):
        "获取事件列表在 `time` 时的值."
        if time - self.lastTime < 16:  # get cache
            maxIter = self.cache + 5
            while not (time in self[self.cache]):
                self.cache += 1
                if self.cache > maxIter or self.cache >= len(self):
                    break
            else:  # exit normally
                return self[self.cache].get(time)
        # break
        self.cache = bisect(self, Event(time, time))-1
        return self[self.cache].get(time)
