from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QSizePolicy, QLabel, QPushButton, QFrame
from gui import MainWindow


class MainMenuBar(QFrame):
    def __init__(self, parent: MainWindow):
        super(MainMenuBar, self).__init__(parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.setGeometry(0, 0, 0, 0)
        self.setFixedHeight(40)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setStyleSheet("background:#3a3a3a; border-bottom: 3px solid #323232;")
        layout = QHBoxLayout(self)
        layout.setAlignment(Qt.AlignLeft)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        back = QPushButton()
        back.setIcon(QIcon("gui/resources/menu.png"))
        back.setMaximumSize(60, 40)
        back.clicked.connect(self.show_menu)
        layout.addWidget(back)
        self.setLayout(layout)

    def show_menu(self):
        self.parent.show_menu()
