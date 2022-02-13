from bisect import bisect

def interpolate(x1, y1, x2, y2, x):
    "返回线性插值."
    try:
        return y1 + (x-x1)*((y2-y1)/(x2-x1))
    except ZeroDivisionError:
        return y1

class Event:
    "基础的事件."
    def __init__(self, startTime, endTime, 
                 start = 0, end = 0, start2 = 0, end2 = 0):
        self.startTime = startTime
        self.endTime = endTime
        self.start = start
        self.end = end
        self.start2 = start2
        self.end2 = end2
    
    def __lt__(self, other): # a < b
        return other.startTime >= self.endTime 

        

class Events(list[Event]):
    def __init__(self, *pra) -> None:
        super().__init__(*pra)

    def get(self,time):
        "获取事件列表在 `time` 时的值."
        event = self[bisect(self, Event(time, time))-1]
        return (interpolate(event.startTime, event.start,
                            event.endTime, event.end,
                            time),
                interpolate(event.startTime, event.start2,
                            event.endTime, event.end2,
                            time))
                
    

