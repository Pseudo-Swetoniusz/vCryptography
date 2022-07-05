from PyQt5.QtWidgets import QFrame, QSizePolicy, QVBoxLayout, QLabel

from gui import MainMenuWindow


class SteganoFrame(QFrame):
    def __init__(self, parent: MainMenuWindow):
        super().__init__(parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.setStyleSheet("background:#3a3a3a; border: 3px solid #323232;")
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout = QVBoxLayout()
        title = QLabel("vCryptography - 1")
        layout.addWidget(title)
        self.setLayout(layout)
        self.setVisible(False)

    def show(self):
        self.setVisible(True)

    def hide(self):
        self.setVisible(False)