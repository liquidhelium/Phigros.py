
from PyQt5.QtWidgets import QLabel

class TimeLableWidget(QLabel):
    def setTime(self, time: int):
        minute =  time // 60
        second = time % 60
        self.setText("{:0>2d}:{:0>2d}".format(minute, second))