from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QApplication, QStyleFactory

from gui.MainMenuBar import MainMenuBar
from gui.MainMenuWindow import MainMenuWindow


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.menu_bar = None
        self.menu_window = None
        self.initUI()
        self.showMaximized()
        self.show()

    def initUI(self):
        widget = QWidget(self)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self.menu_bar = MainMenuBar(self)
        self.menu_window = MainMenuWindow(self)
        layout.addWidget(self.menu_bar)
        layout.addWidget(self.menu_window)
        layout.setAlignment(Qt.AlignCenter)
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        QApplication.setStyle(QStyleFactory.create('Cleanlooks'))
        self.setGeometry(60, 60, 400, 400)
        self.setWindowTitle('vCryptography')
        self.setStyleSheet("background:#4f4f4f;")
        icon = QIcon(r"gui/resources/icon.png")
        self.setWindowIcon(icon)

    def show_menu(self):
        self.menu_window.show_menu()
