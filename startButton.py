from PyQt5.QtWidgets import QPushButton

class startButton(QPushButton):
    def toggleText(self):
        if self.text() == "\ue037": # play_arrow
            self.setText("\ue034") # pause
        else:
            self.setText("\ue037")