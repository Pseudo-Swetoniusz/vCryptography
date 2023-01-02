from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QSizePolicy, QFrame, QHBoxLayout, QPushButton
from gui import MainMenuWindow


class MainMenu(QFrame):
    def __init__(self, parent: MainMenuWindow):
        super().__init__(parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.setStyleSheet("background:#3a3a3a; border: 3px solid #323232;")
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMaximumSize(800, 200)
        layout = QVBoxLayout()
        title = QLabel("vCryptography")
        title.setStyleSheet("color:#aeaeae; border: none;font-size:40px; text-align:center; letter-spacing:3px;")
        title.setFixedHeight(60)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        buttons = ButtonFrame(self)
        layout.addWidget(buttons)
        self.setLayout(layout)

    def send_kimages(self):
        self.parent.init_kimages()

    def send_stego(self):
        self.parent.init_stego()

    def hide(self):
        self.setVisible(False)

    def show(self):
        self.setVisible(True)


class ButtonFrame(QWidget):
    def __init__(self, parent: MainMenu):
        super().__init__(parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        layout = QHBoxLayout()
        button_kimages = QPushButton("Visual Cryptography")
        button_kimages.setMinimumHeight(60)
        button_kimages.setMaximumHeight(100)
        button_kimages.setStyleSheet("QPushButton {color:#9d9d9d; letter-spacing:1px; background:#414141; "
                                     "text-transform:uppercase;font-size:18px;} "
                                     "QPushButton::pressed {background:#515151;}")
        button_kimages.clicked.connect(self.push_kimages)
        button_steganography = QPushButton("steganography")
        button_steganography.setMinimumHeight(60)
        button_steganography.setMaximumHeight(100)
        button_steganography.setStyleSheet("QPushButton {color:#9d9d9d; letter-spacing:1px; background:#414141; "
                                           "text-transform:uppercase;font-size:18px;} "
                                           "QPushButton::pressed {background:#515151;}")
        button_steganography.clicked.connect(self.push_stegano)
        layout.addWidget(button_kimages)
        layout.addWidget(button_steganography)
        self.setLayout(layout)

    def push_kimages(self):
        self.parent.send_kimages()

    def push_stegano(self):
        self.parent.send_stego()
