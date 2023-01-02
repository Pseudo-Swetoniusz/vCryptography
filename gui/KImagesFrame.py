from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QTextEdit, QFrame, QSizePolicy, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QWidget, QComboBox, QGroupBox, QFileDialog, QGridLayout
from algorithm.kimages.vc import VC
from gui import MainMenuWindow
from gui.ErrorMessage import ErrorMessageWindow
from utils.Image import CImage

def throwCustomError(widget, title, message):
    error = ErrorMessageWindow(widget, message, title)
    error.show()

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
        self.main = MainFrame(self)
        layout.addWidget(self.main)
        self.setLayout(layout)
        self.setVisible(False)

    def show(self):
        self.setVisible(True)

    def hide(self):
        self.setVisible(False)

    def restart(self):
        self.main.restart()

class MainFrame(QFrame):
    def __init__(self, parent: KImagesFrame):
        super().__init__(parent)
        self.parent = parent
        self.imagesWidget = None
        self.menuWidget = None
        self.originalPath = None
        self.initUI()

    def initUI(self):
        self.setStyleSheet("background:#434343; border: 3px solid #323232;font: 30pt;")
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

    def setText(self,text):
        self.imagesWidget.setText(text)
    
    def getResultImage(self):
        return self.imagesWidget.getResultImage()

    def saveResultImage(self):
        self.imagesWidget.saveResultImage()

    def getOriginalPath(self):
        return self.originalPath

class ImagesWidget(QWidget):
    def __init__(self, parent: KImagesFrame):
        super().__init__(parent)
        self.parent = parent
        self.original = None
        self.result = None
        self.resultImage = None
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
        # pixmap = image.get_pixmap()
        w, h = self.original.geometry().width(), self.original.geometry().height()
        pixmap = pixmap.scaled(w, h, Qt.KeepAspectRatio)
        self.original.setPixmap(pixmap)

    def setResult(self,image): 
        pixmap = image.get_pixmap()
        w, h = self.result.geometry().width(), self.result.geometry().height()
        pixmap = pixmap.scaled(w, h, Qt.KeepAspectRatio)
        self.result.setPixmap(pixmap)
        self.resultImage = image
    
    def getResultImage(self):
        return self.resultImage

    def setText(self,text):
        self.result.setText(text)
        self.resultImage = None
        self.result.repaint()
    
    def saveResultImage(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name = QFileDialog.getSaveFileName(self, 'Open File', '',
                                                "image Files (*.png)")
        if file_name[0] == '':
            throwCustomError(self.parent, 'error', 'No path selected')
        elif file_name:
            self.resultImage.save_image(file_name[0])
        else:
            throwCustomError(self, 'error', 'error saving image')

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

        self.knValues = ['2','3','4']
        self.algorithms = ['Classic', 'Mixed', 'Improved']
        self.kIdx = 0
        self.nIdx = 0
        self.algoIdx = 0

        self.shares = None
        self.shareIndex = 0
        self.decryptedImg = None
        self.path = None
        self.shareSize = 0
        self.vc = None
        self.width = 600
        self.initUI()

    def initUI(self):
        self.setStyleSheet("background:#3a3a3a; border: 3px solid #323232;color:#9d9d9d;font-size:20px;")
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        layout = QVBoxLayout()

        height = 50
        self.variableInput = VariableInput(self)
        self.variableInput.setMinimumHeight(int(2.2*height))
        self.textInputLabel = QLabel("Input", self)
        self.textInputLabel.setAlignment(Qt.AlignCenter)
        self.textInputLabel.setStyleSheet("background-color:#3a3a3a; border:none; font-size:15; letter-spacing:1px;")
        self.textInputLabel.setMinimumHeight(height)
        self.textInputLabel.setMaximumHeight(height)
        self.imageButton = QPushButton(self)
        self.imageButton.setMinimumHeight(height)
        self.imageButton.setMaximumHeight(height)
        self.imageButton.setMinimumWidth(3*height)
        self.imageButton.setMaximumWidth(3*height)
        self.imageButton.setText("Load Original")
        self.imageButton.clicked.connect(self.loadImage)
        self.startButton = QPushButton(self)
        self.startButton.setMaximumHeight(height)
        self.startButton.setMinimumHeight(height)
        self.startButton.setMinimumWidth(3*height)
        self.startButton.setText("Run")
        self.startButton.clicked.connect(self.run)
        self.shareWidget = ShareWidget(self)
        self.shareImage = QLabel(self)
        self.shareImage.setMaximumHeight(400)
        self.shareImage.setMinimumHeight(400)
        self.shareImage.setMinimumWidth(400)
        self.shareImage.setMaximumWidth(400)
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
            throwCustomError(self, 'Error', 'No image selected')
        elif file_name:
            self.path = file_name[0]
            self.parent.setImage(file_name[0])
        else:
            throwCustomError('No image to save')

    def run(self):
        try:
            self.clearResult("Awaiting result ... ")
            self.clearShares("No shares", "Awaiting shares...")
        except:
            throwCustomError("Error clearing results")
        try:
            k = int(self.knValues[self.kIdx])
            n = int(self.knValues[self.nIdx])
            if(k>n):
                throwCustomError("k must be smaller or equal to n")
                return
            mode = self.algoIdx+1
            self.vc = VC(k,n,mode)
            path = self.parent.getOriginalPath()
            if(path == None):
                throwCustomError(self, 'error', "Image not selected!")
                self.clearResult("Image not selected!")
                self.clearShares("", "")
                return
            img = CImage()
            img.read_image(path)
            self.shares = self.vc(img)
            self.decryptedImg = self.vc.combineShares()
            self.parent.setResult(self.decryptedImg)
            self.prepareShares()
        except:
            throwCustomError(self, 'Error', "Algorithm error")
            self.clearResult("Algorithm error")
            self.clearShares("", "")
    
    def clearShares(self, idxText, shareText):
        self.shareImage.setText(shareText)
        self.shareImage.repaint()
        self.shareWidget.shareLabel.setText(idxText)
        self.shareWidget.shareLabel.repaint()
        self.shares = None

    def clearResult(self,text):
        self.parent.setText(text)
    
    def setShare(self):
        pixmap = self.shares[self.shareIndex].get_pixmap()
        w, h = self.shareImage.geometry().width(), self.shareImage.geometry().height()
        pixmap = pixmap.scaled(w, h, Qt.KeepAspectRatio)
        self.shareImage.setPixmap(pixmap)
    
    def prepareShares(self):
        if(self.shares is None):
            return
        self.shareIndex = 0
        self.shareSize = len(self.shares)
        self.setShare()
        self.shareWidget.setLabel(self.shareIndex)

    def setPrev(self):
        try:
            self.shareIndex = (self.shareIndex-1)%self.shareSize
            self.setShare()
            self.shareWidget.setLabel(self.shareIndex)
        except ZeroDivisionError:
            throwCustomError(self, 'Error', "No shares to show!")
        except:
            throwCustomError(self, 'Error', "Next share error")

    def setNext(self):
        try:
            self.shareIndex = (self.shareIndex+1)%self.shareSize
            self.setShare()
            self.shareWidget.setLabel(self.shareIndex)
        except ZeroDivisionError:
            throwCustomError(self, 'Error', "No shares to show!")
        except:
            throwCustomError(self, 'Error', "Next share error")


class VariableInput(QWidget):
    def __init__(self,parent: KImagesFrame):
        super().__init__(parent)
        self.parent = parent
        self.gridGroupBox = None
        self.kLayout = None
        self.algoInput = None
        self.kLabel = None
        self.nLabel = None
        self.algoLabel = None
        self.initUI()

    def initUI(self):
        self.setMinimumWidth(600)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        self.createHorizontalLayout()
        layout.addWidget(self.gridGroupBox)
        self.setLayout(layout)

    def createHorizontalLayout(self):
        self.gridGroupBox = QGroupBox()
        grid_layout = QGridLayout()

        kLabel = QLabel("Input k", self)
        kLabel.setStyleSheet("border: none")
        nLabel = QLabel("Input n", self)
        nLabel.setStyleSheet("border: none")
        algoLabel = QLabel("Algo", self)
        algoLabel.setStyleSheet("border: none")
        kInput = QComboBox()
        kInput.addItems(self.parent.knValues)
        kInput.currentIndexChanged.connect(self.k_index_changed)
        nInput = QComboBox()
        nInput.addItems(self.parent.knValues)
        nInput.currentIndexChanged.connect(self.n_index_changed)
        algoInput = QComboBox()
        algoInput.addItems(self.parent.algorithms)
        algoInput.currentIndexChanged.connect(self.algo_index_changed)

        grid_layout.addWidget(kLabel,0,0)
        grid_layout.addWidget(nLabel,0,1)
        grid_layout.addWidget(algoLabel,0,2)
        grid_layout.addWidget(kInput,1,0)
        grid_layout.addWidget(nInput,1,1)
        grid_layout.addWidget(algoInput,1,2)
        self.gridGroupBox.setLayout(grid_layout)

    def k_index_changed(self, index):
        self.parent.kIdx = index

    def n_index_changed(self, index):
        self.parent.nIdx = index

    def algo_index_changed(self, index):
        self.parent.algoIdx = index

class CombineWidget(QWidget):
    def __init__(self,parent: KImagesFrame):
        super().__init__(parent)
        self.parent = parent
        self.idxInput = None
        self.combineButton = None
        self.saveButton = None
        self.currentImage = None
        self.initUI()

    def initUI(self):
        self.setMinimumWidth(600)
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
        self.saveButton = QPushButton('Save', self)
        self.saveButton.clicked.connect(self.save)
        layout.addWidget(self.saveButton)

        self.horizontalGroupBox.setLayout(layout)

    def combine(self):
        indices = []
        try:
            variableString = self.idxInput.toPlainText()
            indices = list(map(int, variableString.split(' ')))
        except:
            throwCustomError(self, 'Error', "Failed to get input")
            return
        try:
            combinedImg = self.parent.vc.combineSharesByIdx(indices)
            if(combinedImg == None):
                throwCustomError(self, 'Error', "Improper indices")
            else:
                self.parent.parent.setResult(combinedImg)
        except:
            throwCustomError(self, 'Error', "problem combining")

    def save(self):
        try:
            img = self.parent.parent.getResultImage()
            self.parent.parent.saveResultImage()
        except:
            throwCustomError(self, 'Error', "Error saving image")


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


