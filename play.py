from PhiPlayer.Player import PhiPlayer
from PyQt5.QtWidgets import QApplication,QMainWindow

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
    window1.setGeometry(0,0,800,600)
    window.setParent(window1)
    window1.setCentralWidget(window)
    window1.show()
    app.exec()