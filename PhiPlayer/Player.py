from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog,QWidget
from .GUI_phi import Ui_PhiPlayer
from .integrated import IntegratedPlayer


class PhiPlayer(QMainWindow):
    def __init__(self, *args) -> None:
        super().__init__(*args)
        self.ui = Ui_PhiPlayer()
        self.ui.setupUi(self)
        
    def openFileToRead(self):
        player = self.findChild(IntegratedPlayer,"player")
        dialog = QFileDialog()
        filters = \
        [
            "Phigros 官谱 (*.json)",
            "图片文件 (*.png)",
            "所有文件 (*)"
        ]

        file = dialog.getOpenFileName(
            caption = "打开可用文件", 
            filter=";;".join(filters)
        )
        if file[1] == filters[0]:
            player.loadSong(chartAddr=file[0])
        elif file[1] == filters[1]:
            player.loadSong(illustrationAddr=file[0])
        else:
            player.loadSong(chartAddr=file[0])
    
    def loadSong(self, illustrationAddr=None, musicAddr=None, chartAddr=None,):
        self.ui.player.loadSong(illustrationAddr,musicAddr,chartAddr)

    def setRatio(self, a0:int, a1:int):
        self.ui.ratioKeeper.setRatio(a0,a1)
            
            


if __name__ == "__main__":
    app = QApplication([])
    window = PhiPlayer()
    window.loadSong(
        chartAddr="./assets/Introduction_Chart.json",
        musicAddr="./assets/Introduction.mp3",
        illustrationAddr="./assets/IllustrationBlur.png",
        )
    window.setRatio(16,9)
    window1 = QMainWindow()
    window.setParent(window1)
    window1.setCentralWidget(window)
    window1.show()
    app.exec()

