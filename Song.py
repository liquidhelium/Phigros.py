from PyQt5.QtGui import QImage, QColor
from Chart import Chart

class Song:
    cover = QImage(1000, 1000, QImage.Format(QImage.Format.Format_RGBA64))
    cover.fill(QColor(0,0,0,128))
    def __init__(self, chart: Chart, illustration: QImage = None):
        self.chart=chart
        self.illustration=illustration.mirrored(False,True)