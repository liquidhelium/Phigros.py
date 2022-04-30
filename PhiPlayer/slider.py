from PyQt5.QtWidgets import QSlider
from PyQt5.QtGui import QMouseEvent


class SeekBar(QSlider):
    def mousePressEvent(self, ev: QMouseEvent) -> None:
        super().mousePressEvent(ev)
        val_por = ev.pos().x() / self.width()    # 获取鼠标在进度条的相对位置
        self.setValue(int(val_por * self.maximum()))  # 改变进度条的值
        self.sliderMoved.emit(int(val_por * self.maximum()))
