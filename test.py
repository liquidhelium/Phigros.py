import PhiPlayer

from PyQt5.QtWidgets import QApplication, QGraphicsView,QGraphicsScene, QGraphicsRectItem, QGraphicsItemGroup, QWidget, QMainWindow, QGraphicsPixmapItem
from PyQt5.QtGui import QTransform
from PyQt5.QtCore import QTimer, QTimerEvent
import time
chartAddr="./assets/Introduction_Chart.json"

file = open(chartAddr)



app = QApplication([])
window = QMainWindow()

chart = PhiPlayer.officalChartLoader.officalChartLoader(file)


win = QMainWindow()
wid = QWidget(win)
# win.setCentralWidget(wid)
sce = QGraphicsScene()
sce.setSceneRect(0,0,800,600)

from PhiPlayer.Line_new import GuiLine

# line = chart.lines[0]

# guiline = GuiLine(None,line)
guilines = [GuiLine(None,line) for line in chart.lines]
for i in guilines:
    sce.addItem(i)
    i.updateState(0)
timeNow = time.perf_counter()
def handle():
    for i in guilines:
        i.updateState(time.perf_counter() - timeNow + 25)

timer = QTimer()
timer.setInterval(10)
timer.timeout.connect(handle)
timer.start()


view = QGraphicsView(sce)

trans = QTransform()
trans.rotate(180)
view.setTransform(trans)
view.setBaseSize(800,600)
view.centerOn(400,300)
view.setViewport(wid)
view.setDragMode(1)

# group.setRotation(-60)
# r1.setRotation(60)
# r1.setRotation(0)
# group.setRotation(0)
# view.show()
win.setCentralWidget(view)
win.show()
app.exec()