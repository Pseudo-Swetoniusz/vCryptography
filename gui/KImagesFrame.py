from PyQt5.QtWidgets import QFrame, QSizePolicy, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QRect
from algorithm.kimages.test_vc import run
from gui import MainMenuWindow


class KImagesFrame(QFrame):
    def __init__(self, parent: MainMenuWindow):
        super().__init__(parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.path = "algorithm\\kimages\\test_img\\penta.png"
        self.setStyleSheet("background:#3a3a3a; border: 3px solid #323232;")
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout = QVBoxLayout()
        # title = QLabel("vCryptography - 2")
        # layout.addWidget(title)
        self.photo = QLabel()
        self.photo.setGeometry(QRect(0,0,421,256)) #0,0,421,256 #0, 0, 841, 511
        self.photo.setPixmap(QPixmap(self.path))
        self.photo.setScaledContents(True)
        self.left = QPushButton()
        self.left.setGeometry(QRect(0,255,206,21)) #0,255,206,21 #0, 510, 411, 41
        self.right = QPushButton()
        self.right.setGeometry(QRect(205,255,191,21)) #205,255,191,21 #410, 510, 391, 41
        self.left.clicked.connect(self.show_picture)
        self.right.clicked.connect(self.show_picture)
        layout.addWidget(self.photo)
        layout.addWidget(self.left)
        layout.addWidget(self.right)

        self.setLayout(layout)
        self.setVisible(False)
    
    def show_picture(self):
        self.photo.setPixmap(QPixmap("algorithm\\kimages\\test_img\\really-big-picture.jpg"))

    def show(self):
        self.setVisible(True)

    def hide(self):
        self.setVisible(False)

    def run(sel,n,k,orig_path):
        shares,decrypted_image = run(n,orig_path)
        return shares,decrypted_image
