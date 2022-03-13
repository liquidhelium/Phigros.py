from PyQt5.QtWidgets import QFrame, QWidget
from PyQt5.QtGui import QResizeEvent
from PyQt5.QtCore import QSize


class KeepRatioWidget(QFrame):
    def setRatio(self, width: int, height: int):
        self.widthRatio = width
        self.heightRatio = height
        self.resize(self.size())# initial put

    
    def resizeEvent(self, a0: QResizeEvent) -> None:
        old = a0.size()
        new = a0.size()
        childs:list[QWidget] = self.children()
        if len(childs) > 1:
            raise ValueError("KeepRadioWidget: Too many childs")
        child = childs[0]
        if new.width() < self.widthRatio * new.height() / self.heightRatio:
            new.setHeight(int(self.heightRatio * new.width() / self.widthRatio))
            child.move(0,int((old.height()-new.height())/2))
        else:
            new.setWidth(int(self.widthRatio * new.height() / self.heightRatio))
            child.move(int((old.width()-new.width())/2),0)
        child.resize(new)
        return super().resizeEvent(a0)
