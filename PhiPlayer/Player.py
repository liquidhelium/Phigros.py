from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QWidget
from .GUI_player import Ui_Player
from .integrated import IntegratedPlayer
import pickle

MAGIC_NUMBER = b"PhiChart"

class PhiPlayer(QWidget):
    def __init__(self, *args) -> None:
        super().__init__(*args)
        self.ui = Ui_Player()
        self.ui.setupUi(self)

    def openFileToRead(self):
        player = self.ui.player
        dialog = QFileDialog()
        filters = \
            [
                "Phigros 官谱 (*.json)",
                "自定义谱面 (*.phi)",
                "图片文件 (*.png)",
                "所有文件 (*)"
            ]

        file = dialog.getOpenFileName(
            caption="打开可用文件",
            filter=";;".join(filters)
        )
        if file[1] == filters[0]:
            player.loadSong(chartAddr=file[0])
        elif file[1] == filters[1]:
            with open(file[0], "rb") as f:
                if not f.read(len(MAGIC_NUMBER)) == MAGIC_NUMBER:
                    raise ValueError("Bad magic number, this is not a chart")
                f.readline()
                player.song.chart = pickle.load(f)
                player.loadSong()
        elif file[1] == filters[2]:
            player.loadSong(illustrationAddr=file[0])
        
        else:
            player.loadSong(chartAddr=file[0])

    def loadSong(self, illustrationAddr=None, musicAddr=None, chartAddr=None,):
        self.ui.player.loadSong(illustrationAddr, musicAddr, chartAddr)

    def setRatio(self, a0: int, a1: int):
        self.ui.ratioKeeper.setRatio(a0, a1)

    def pause(self):
        self.ui.player.pause()

    def play(self):
        self.ui.player.start()

    def toogle(self):
        self.ui.player.toggle()
    
    def saveChart(self):
        file = open("test.phi", "wb")
        file.write(b"PhiChart v1.0 alpha\n")
        pickle.dump(self.ui.player.chart, file)



if __name__ == "__main__":
    app = QApplication([])
    window = PhiPlayer()
    window.loadSong(
        chartAddr="./assets/Introduction_chart.json",
        musicAddr="./assets/Introduction.mp3",
        illustrationAddr="./assets/IllustrationBlur.png",
    )
    window.setRatio(16, 9)
    window1 = QMainWindow()
    window.setParent(window1)
    window1.setCentralWidget(window)
    window1.show()
    app.exec()
