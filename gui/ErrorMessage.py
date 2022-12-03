import string

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QLabel, QWidget, QVBoxLayout, QPushButton


class ErrorMessageWindow(QMainWindow):
    def __init__(self, parent, error_message: string, error_title: string):
        super(ErrorMessageWindow, self).__init__(parent)
        self.error_message = error_message
        self.error_title = error_title
        self.error_label = QLabel()
        self.exit_button = QPushButton("exit")
        self.main_widget = QWidget()
        self.initUI()

    def initUI(self):
        print("iwbouiwbof")
        self.setWindowTitle(self.error_title)
        layout = QVBoxLayout()
        self.setCentralWidget(self.main_widget)
        self.setGeometry(500, 120, 0, 0)
        print("uwbfuwbfiuwfb")
        self.setStyleSheet("background:#3a3a3a; border: 2px solid #323232;")
        print("uwbfuwbfiuwfb 2")
        self.error_label.setMaximumWidth(500)
        self.error_label.setMinimumWidth(500)
        print("uwbfuwbfiuwfb 3")
        self.error_label.setAlignment(Qt.AlignCenter)
        self.error_label.setStyleSheet("background:#323232; color:#9d9d9d;")
        self.error_label.setText(self.error_message)
        print("uwbfuwbfiuwfb 4")
        print("uwbfuwbfiuwfb 5")
        self.exit_button.setStyleSheet("QPushButton {color:#9d9d9d; letter-spacing:1px; background:#414141; "
                                       "text-transform:uppercase;font-size:13px; padding-top:2px; padding-bottom:2px;} "
                                       "QPushButton::pressed {background:#515151;}")
        print("wwuwgbuwigw")
        self.exit_button.clicked.connect(self.exit_window)
        layout.addWidget(self.error_label)
        layout.addWidget(self.exit_button)
        self.main_widget.setLayout(layout)
        print("wibfuwbfgui")
        self.resize(500, 120)
        self.show()

    def exit_window(self):
        self.close()
