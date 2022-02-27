from PyQt5.QtWidgets import QMainWindow, QApplication
from GUI_phi import Ui_MainWindow


app = QApplication([])
window = QMainWindow()
UI = Ui_MainWindow()
UI.setupUi(window)
UI.player.loadSong(
        chartAddr="assets/Chart_IN_Error",
        musicAddr="assets/Introduction.mp3",
        illustrationAddr="./assets/IllustrationBlur.png",
        )
UI.ratioKeeper.setRatio(16,9)
window.show()
app.exec()
