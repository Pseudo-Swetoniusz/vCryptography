import sys
from PyQt5.QtWidgets import QApplication

from gui.MainWindow import MainWindow

def main(arg):
    app = QApplication(arg)
    gui = MainWindow()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main(sys.argv)