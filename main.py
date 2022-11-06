import sys
from PyQt5.QtWidgets import QApplication

from gui.MainWindow import MainWindow
# classic 3,3 not working

def main(arg):
    app = QApplication(arg)
    gui = MainWindow()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main(sys.argv)