from Events import Event, Events
import profile
import line_profiler
from View import newPainter
from Song import Song
from officalChartLoader import officalChartLoader
from PyQt5.QtGui import QImage, QPixmap, QGuiApplication

p = line_profiler.LineProfiler()
def preWork():
    chartAddr="assets/Chart_IN_Error"
    illustrationAddr="./assets/IllustrationBlur.png"
    illustration = QImage(illustrationAddr)
    f = open(chartAddr)
    chart = officalChartLoader(f)
    f.close()
    global song
    song = Song(
        chart,
        illustration
    )
    global picmap
    picmap = QPixmap(1920,1080)
    global time
    time = 90.0 # s

def render():
    global picmap
    global time
    global song
    painter = newPainter()
    painter.begin(picmap)
    painter.setWindow(0, picmap.height(), picmap.width(), -picmap.height())
    painter.drawSong(time, song)
    painter.end()

if __name__ == "__main__":
    app = QGuiApplication([])
    preWork()
    render()
    newPainter.drawSong = p(newPainter.drawSong)
    newPainter.drawNote = p(newPainter.drawNote)
    newPainter.drawJudgeLine = p(newPainter.drawJudgeLine)
    Events.get = p(Events.get)
    
    render()
    p.print_stats()