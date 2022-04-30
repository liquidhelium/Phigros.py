from PyQt5.QtWidgets import QPushButton


class startButton(QPushButton):
    def toggleText(self):
        if self.text() == "\ue037":
            self.setPlay()
        else:
            self.setPause()

    def setPause(self):
        self.setText("\ue034")  # pause

    def setPlay(self):
        self.setText("\ue037")  # play_arrow
