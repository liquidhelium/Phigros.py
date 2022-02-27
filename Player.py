from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QDialog
from GUI_phi import Ui_PhiPlayer


class PhiPlayer(Ui_PhiPlayer):
    def setupUi(self, PhiPlayer):
        super().setupUi(PhiPlayer)
        self.actionOpen.triggered.connect(self.openFileToRead)

    def openFileToRead(self):
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
            self.player.loadSong(chartAddr=file[0])
        elif file[1] == filters[1]:
            self.player.loadSong(illustrationAddr=file[0])
            
            

        
    
app = QApplication([])
window = QMainWindow()
UI = PhiPlayer()
UI.setupUi(window)
UI.player.loadSong(
    chartAddr="assets/Chart_IN_Error",
    musicAddr="assets/Introduction.mp3",
    illustrationAddr="./assets/IllustrationBlur.png",
    )
UI.ratioKeeper.setRatio(16,9)
window.show()
app.exec()
