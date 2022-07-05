from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSizePolicy, QVBoxLayout, QFrame
from gui import MainWindow, KImagesFrame, SteganoFrame
from gui.MainMenu import MainMenu
from gui.SteganoFrame import SteganoFrame
from gui.KImagesFrame import KImagesFrame

class MainMenuWindow(QFrame):
    def __init__(self, parent: MainWindow):
        super().__init__(parent)
        self.layout = None
        self.menu = None
        self.k_images = None
        self.stegano = None
        self.initUI()
        self.window = parent

    def initUI(self):
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.menu = MainMenu(self)
        self.stegano = SteganoFrame(self)
        self.k_images = KImagesFrame(self)
        self.layout.addWidget(self.menu)
        self.layout.addWidget(self.k_images)
        self.layout.addWidget(self.stegano)
        self.layout.setAlignment(Qt.AlignCenter)
        self.setLayout(self.layout)

    def init_kimages(self):
        self.menu.hide()
        self.k_images.show()

    def init_stego(self):
        self.menu.hide()
        self.stegano.show()

    def show_menu(self):
        self.menu.show()
        self.stegano.hide()
        self.k_images.hide()