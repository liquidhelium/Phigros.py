import pyjion;
pyjion.enable()
pyjion.config(pgc=True,level=1)
from PhiPlayer.GUI_phi import Ui_win
from PyQt5.QtWidgets import QApplication, QMainWindow

if __name__ == "__main__":
    app = QApplication([])
    window = QMainWindow()
    ui = Ui_win()
    ui.setupUi(window)
    ui.player.loadSong(
        chartAddr="./assets/Introduction_chart.json",
        musicAddr="./assets/Introduction.mp3",
        illustrationAddr="./assets/IllustrationBlur.png",
    )
    ui.player.setRatio(16, 9)
    window.show()
    app.exec()
