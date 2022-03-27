from PyQt5.QtGui import QImage, QColor
from Chart import Chart

class Song:
    cover = QImage(500, 500, QImage.Format(QImage.Format.Format_ARGB32))
    cover.fill(QColor(0,0,0,128))
    def __init__(self, chart: Chart, illustration: QImage = None):
        self.coverCacheRes = (0,0)
        self.coverCache = None
        self.chart=chart
        self.illustration=illustration.mirrored(False,True)
        self.illustrationCache = None
        self.illustrationCacheRes = (0,0)