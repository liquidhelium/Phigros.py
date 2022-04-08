from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from GUI_phi import Ui_PhiPlayer
from integrated import IntegratedPlayer


class PhiPlayer(QMainWindow):
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
            
            


if __name__ == "__main__":
    app = QApplication([])
    window = PhiPlayer()
    UI = Ui_PhiPlayer()
    UI.setupUi(window)
    UI.player.loadSong(
        chartAddr="assets/Introduction_Chart.json",
        musicAddr="assets/Introduction.mp3",
        illustrationAddr="./assets/IllustrationBlur.png",
        )
    UI.ratioKeeper.setRatio(16,9)
    window1 = QMainWindow()
    window.setParent(window1)
    window1.setCentralWidget(window)
    window1.show()
    app.exec()

