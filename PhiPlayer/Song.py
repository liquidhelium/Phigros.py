from PyQt5.QtGui import QPixmap, QColor, QTransform
from PyQt5.QtCore import Qt
from .Chart import Chart


class Song:

    def __init__(self, chart: Chart, illustration: QPixmap = None):
        trans = QTransform()
        trans.rotate(180, Qt.Axis.XAxis)
        self.cover = QPixmap(50, 50)
        self.cover.fill(QColor(0, 0, 0, 128))
        self.coverCacheRes = (0, 0)
        self.coverCache = None
        self.chart = chart
        self.illustration = illustration.transformed(trans)
        self.illustrationCache = None
        self.illustrationCacheRes = (0, 0)
