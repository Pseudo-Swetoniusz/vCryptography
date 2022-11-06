from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QTextEdit, QFrame, QSizePolicy, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QWidget, QGraphicsView, QGroupBox, QFileDialog

from algorithm.kimages.vc import VC
from gui import MainMenuWindow

from utils.Image import CImage

# fix bugs, damage control, make it look better?

class KImagesFrame(QFrame):
    def __init__(self, parent: MainMenuWindow):
        super().__init__(parent)
        self.parent = parent
        self.main = None
        self.initUI()

    def initUI(self):
        self.setStyleSheet("background:#3a3a3a; border: 3px solid #323232;")
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        menu = MenuBar(self)
        self.main = MainFrame(self)
        layout.addWidget(menu)
        layout.addWidget(self.main)
        self.setLayout(layout)
        self.setVisible(False)

    def show(self):
        self.setVisible(True)

    def hide(self):
        self.setVisible(False)

    def restart(self):
        self.main.restart()

class MenuBar(QFrame):
    def __init__(self, parent: KImagesFrame):
        super().__init__(parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.setGeometry(0, 0, 0, 0)
        self.setFixedHeight(40)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setStyleSheet("background:#323232; border: 3px solid #323232;")
        layout = QHBoxLayout(self)
        layout.setAlignment(Qt.AlignRight)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        back = QPushButton()
        back.setIcon(QIcon("gui/resources/back_arrow.png"))
        back.setMaximumSize(60, 40)
        back.clicked.connect(self.restart)
        layout.addWidget(back)
        self.setLayout(layout)

    def restart(self):
        self.parent.restart()

class MainFrame(QFrame):
    def __init__(self, parent: KImagesFrame):
        super().__init__(parent)
        self.parent = parent
        self.imagesWidget = None
        self.menuWidget = None
        self.originalPath = None
        self.initUI()

    def initUI(self):
        self.setStyleSheet("background:#434343; border: 3px solid #323232;")
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout = QHBoxLayout(self)
        self.imagesWidget = ImagesWidget(self)
        self.menuWidget = MenuWidget(self)

        layout.addWidget(self.imagesWidget)
        layout.addWidget(self.menuWidget)
        self.setLayout(layout)

    def setImage(self, path):
        pixmap = QPixmap(path)
        self.imagesWidget.setOriginal(pixmap)
        self.originalPath = path

    def setResult(self,image):
        self.imagesWidget.setResult(image)

    def getOriginalPath(self):
        return self.originalPath

class ImagesWidget(QWidget):
    def __init__(self, parent: KImagesFrame):
        super().__init__(parent)
        self.original = None
        self.result = None
        self.initUI()

    def initUI(self):
        self.setMinimumWidth(1200)
        self.setMaximumWidth(1200)
        self.setStyleSheet("background:#3a3a3a; border: 3px solid #323232;")
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        
        height = 800

        self.original = QLabel(self)
        self.original.setMinimumHeight(height//2)
        self.original.setMaximumHeight(height//2)
        self.original.setAlignment(Qt.AlignCenter)
        self.result = QLabel(self)
        self.result.setMinimumHeight(height//2)
        self.result.setMaximumHeight(height//2)
        self.result.setAlignment(Qt.AlignCenter)
        
        layout.addWidget(self.original)
        layout.addWidget(self.result)
        self.setLayout(layout)

    def setOriginal(self,pixmap):
        w, h = self.original.geometry().width(), self.original.geometry().height()
        pixmap = pixmap.scaled(w, h, Qt.KeepAspectRatio)
        self.original.setPixmap(pixmap)

    def setResult(self,pixmap):
        w, h = self.result.geometry().width(), self.result.geometry().height()
        pixmap = pixmap.scaled(w, h, Qt.KeepAspectRatio)
        self.result.setPixmap(pixmap)

class MenuWidget(QWidget):
    def __init__(self, parent: KImagesFrame):
        super().__init__(parent)
        self.parent = parent
        self.textInputLabel = None
        self.imageButton = None
        self.variableInput = None
        self.startButton = None
        self.shareWidget = None
        self.shareImage = None
        self.combineWidget = None

        self.shares = None
        self.shareIndex = 0
        self.decryptedImg = None
        self.path = None
        self.shareSize = 0
        self.vc = None
        self.width = 600
        self.initUI()

    def initUI(self):
        self.setMinimumWidth(self.width)
        self.setStyleSheet("background:#3a3a3a; border: 3px solid #323232;color:#9d9d9d;font-size:20px;")
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        
        layout = QVBoxLayout()
        # layout.setAlignment(Qt.AlignHCenter)

        height = 50
        self.variableInput = QTextEdit(self)
        self.variableInput.setStyleSheet("background-color:#3a3a3a;border:none;font-size:30px; letter-spacing:1px;")#pink
        self.variableInput.setMinimumHeight(height)
        self.variableInput.setMaximumHeight(height)
        self.textInputLabel = QLabel("Input", self)
        self.textInputLabel.setAlignment(Qt.AlignCenter)
        self.textInputLabel.setStyleSheet("background-color:#3a3a3a;border:none;font-size:30px; letter-spacing:1px;") #yellow
        self.textInputLabel.setMinimumHeight(height)
        self.textInputLabel.setMaximumHeight(height)
        self.imageButton = QPushButton(self)
        self.imageButton.setMinimumHeight(height)
        self.imageButton.setMaximumHeight(height)
        self.imageButton.setMinimumWidth(3*height)
        self.imageButton.setMaximumWidth(3*height)
        self.imageButton.setText("Load Original")
        self.imageButton.clicked.connect(self.loadImage)
        # self.startButton = QPushButton(self)
        self.startButton = StartWidget(self)
        self.startButton.setMinimumHeight(height)
        # self.startButton.setMaximumHeight(height)
        self.startButton.setMinimumWidth(3*height)
        # self.startButton.setMaximumWidth(3*height)
        # self.startButton.setText("Run")
        # self.startButton.clicked.connect(self.run)
        self.shareWidget = ShareWidget(self)
        self.shareImage = QLabel(self)
        # self.shareImage.setMinimumHeight(self.width*0.8)
        x = 0.5
        self.shareImage.setMinimumWidth(int(self.width*x))
        self.shareImage.setMaximumHeight(int(self.width*x))
        self.shareImage.setMaximumWidth(int(self.width*x))
        self.shareImage.setAlignment(Qt.AlignCenter)
        self.combineWidget = CombineWidget(self)
        self.combineWidget.setMinimumHeight(3*height)
        self.combineWidget.setMaximumHeight(3*height)
        
        layout.addWidget(self.textInputLabel)
        layout.addWidget(self.imageButton, alignment=Qt.AlignHCenter)
        layout.addWidget(self.variableInput)
        layout.addWidget(self.startButton, alignment=Qt.AlignHCenter)
        layout.addWidget(self.shareWidget, alignment=Qt.AlignHCenter)
        layout.addWidget(self.shareImage, alignment=Qt.AlignHCenter)
        layout.addWidget(self.combineWidget, alignment=Qt.AlignHCenter)

        self.setLayout(layout)

    def loadImage(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name = QFileDialog.getOpenFileName(self, 'Open File', '', "image Files (*.png)")
        if file_name[0] == '':
            print('filename error')
        elif file_name:
            self.path = file_name[0]
            self.parent.setImage(file_name[0])
        else:
            print('load image error')

    def run(self, mode=3):
        try:
            variableString = self.variableInput.toPlainText()
            intList = list(map(int, variableString.split(' ')))
        except:
            print("failed to get args :(")
            return
        if(len(intList)!=2):
            print("Wrong number of args")
        else:
            k,n = intList
            self.vc = VC(k,n,mode)
            path = self.parent.getOriginalPath()
            if(path == None):
                print("image not selected!")
                return
            img = CImage()
            img.read_image(path)
            print(n,img.get_pixmap())
            self.shares = self.vc(img)
            self.decryptedImg = self.vc.combineShares()
            self.parent.setResult(self.decryptedImg.get_pixmap())
            self.prepareShares()

    def setClassic(self):
        self.run(1)

    def setMixed(self):
        self.run(2)

    def setImproved(self):
        self.run(3)
    
    def setShare(self):
        pixmap = self.shares[self.shareIndex].get_pixmap()
        w, h = self.shareImage.geometry().width(), self.shareImage.geometry().height()
        pixmap = pixmap.scaled(w, h, Qt.KeepAspectRatio)
        self.shareImage.setPixmap(pixmap)
    
    def prepareShares(self):
        if(self.shares is None):
            print("no shares")
            return
        self.shareIndex = 0
        self.shareSize = len(self.shares)
        self.setShare()
        self.shareWidget.setLabel(self.shareIndex)

    def setPrev(self):
        self.shareIndex = (self.shareIndex-1)%self.shareSize
        self.setShare()
        self.shareWidget.setLabel(self.shareIndex)

    def setNext(self):
        self.shareIndex = (self.shareIndex+1)%self.shareSize
        self.setShare()
        self.shareWidget.setLabel(self.shareIndex)

class CombineWidget(QWidget):
    def __init__(self,parent: KImagesFrame):
        super().__init__(parent)
        self.parent = parent
        self.idxInput = None
        self.combineButton = None
        self.initUI()

    def initUI(self):
        self.setMinimumWidth(600)
        self.setStyleSheet("background:##008080; border: 3px solid #323232;")
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        self.createHorizontalLayout()
        layout.addWidget(self.horizontalGroupBox)
        self.setLayout(layout)

    def createHorizontalLayout(self):
        self.horizontalGroupBox = QGroupBox()
        layout = QHBoxLayout()
        self.horizontalGroupBox.setMaximumHeight(80)

        self.idxInput = QTextEdit(self)
        self.idxInput.setStyleSheet("background-color:#3a3a3a;border:none;font-size:30px; letter-spacing:1px;")
        self.idxInput.setMinimumHeight(50)
        self.idxInput.setMaximumHeight(50)
        layout.addWidget(self.idxInput)
        self.combineButton = QPushButton('Combine', self)
        self.combineButton.clicked.connect(self.combine)
        layout.addWidget(self.combineButton)

        self.horizontalGroupBox.setLayout(layout)

    def combine(self):
        indices = []
        try:
            variableString = self.idxInput.toPlainText()
            indices = list(map(int, variableString.split(' ')))
            # print("combine: ", indices)
        except:
            print("failed to get input :(")
            return
        try:
            combinedImg = self.parent.vc.combineSharesByIdx(indices)
            self.parent.parent.setResult(combinedImg.get_pixmap())
        except:
            print("problem combining")
        

class StartWidget(QWidget):
    def __init__(self, parent: KImagesFrame):
        super().__init__(parent)
        self.parent = parent
        self.classicButton = None
        self.mixedButton = None
        self.improvedButton = None
        self.initUI()

    def initUI(self):
        self.setMinimumWidth(400)
        self.setStyleSheet("background:#3a3a3a; border: 3px solid #323232;")
        self.setMaximumHeight(100)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        self.createHorizontalLayout()
        layout.addWidget(self.horizontalGroupBox)
        self.setLayout(layout)

    def createHorizontalLayout(self):
        self.horizontalGroupBox = QGroupBox()
        layout = QHBoxLayout()
        self.horizontalGroupBox.setMinimumHeight(100)
        self.horizontalGroupBox.setMaximumHeight(100)
        self.classicButton = QPushButton('Classic', self)
        self.classicButton.clicked.connect(self.parent.setClassic)
        layout.addWidget(self.classicButton)
        self.mixedButton = QPushButton('Mixed', self)
        self.mixedButton.clicked.connect(self.parent.setMixed)
        layout.addWidget(self.mixedButton)
        self.improvedButton = QPushButton('Inproved', self)
        self.improvedButton.clicked.connect(self.parent.setImproved)
        layout.addWidget(self.improvedButton)

        self.horizontalGroupBox.setLayout(layout)


class ShareWidget(QWidget):
    def __init__(self, parent: KImagesFrame):
        super().__init__(parent)
        self.parent = parent
        self.prevButton = None
        self.nextButton = None
        self.shares = None
        self.shareLabel = None
        self.initUI()

    def initUI(self):
        self.setMinimumWidth(400)
        self.setStyleSheet("background:#3a3a3a; border: 3px solid #323232;")
        self.setMaximumHeight(100)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        self.createHorizontalLayout()
        layout.addWidget(self.horizontalGroupBox)
        self.setLayout(layout)

    def createHorizontalLayout(self):
        self.horizontalGroupBox = QGroupBox()
        layout = QHBoxLayout()
        self.horizontalGroupBox.setMinimumHeight(100)
        self.horizontalGroupBox.setMaximumHeight(100)

        self.prevButton = QPushButton('Prev', self)
        self.prevButton.clicked.connect(self.parent.setPrev)
        layout.addWidget(self.prevButton)
        
        self.shareLabel = QLabel("", self)
        self.shareLabel.setAlignment(Qt.AlignCenter)
        self.shareLabel.setStyleSheet("background:#3a3a3a; border: none")
        layout.addWidget(self.shareLabel)
        
        self.nextButton = QPushButton('Next', self)
        self.nextButton.clicked.connect(self.parent.setNext)
        layout.addWidget(self.nextButton)
        
        self.horizontalGroupBox.setLayout(layout)

    def setLabel(self, idx):
        self.shareLabel.setText(f"Share {idx}")


