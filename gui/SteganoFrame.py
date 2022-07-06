from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap, QColor
from PyQt5.QtWidgets import QFrame, QSizePolicy, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QWidget, QFileDialog, \
    QGridLayout

from algorithm.steganography.LSBSteganography import LSBSteganography
from gui import MainMenuWindow


class SteganoFrame(QFrame):
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
        menu = SteganoMenuBar(self)
        self.main = SteganoMainFrame(self)
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


class SteganoMenuBar(QFrame):
    def __init__(self, parent: SteganoFrame):
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


class SteganoMainFrame(QFrame):
    def __init__(self, parent: SteganoFrame):
        super().__init__(parent)
        self.rd_widget = None
        self.rt_widget = None
        self.ri_widget = None
        self.i3 = None
        self.i2t = None
        self.initUI()

    def initUI(self):
        self.setStyleSheet("background:#434343; border: 3px solid #323232;")
        layout = QHBoxLayout(self)
        self.rd_widget = ReadDecideWidget(self)
        self.rt_widget = ReadTextWidget(self)
        self.ri_widget = ReadImageWidget(self)
        self.i3 = ImageInImageWidget(self)
        self.i2t = TextInImageWidget(self)
        layout.addWidget(self.rd_widget)
        layout.addWidget(self.rt_widget)
        layout.addWidget(self.ri_widget)
        layout.addWidget(self.i3)
        layout.addWidget(self.i2t)
        self.setLayout(layout)

    def read_text(self, path):
        print("read text 2")
        self.rd_widget.hide()
        self.rt_widget.set_results(path)

    def read_image(self, path):
        print("read image 2")
        self.rd_widget.hide()
        self.ri_widget.set_results(path)

    def restart(self):
        self.ri_widget.hide()
        self.rt_widget.hide()
        self.i3.hide()
        self.i2t.hide()
        self.rd_widget.show()

    def image_in_image(self, path):
        print('im1')
        self.rd_widget.hide()
        self.i3.set_results(path)

    def text_in_image(self, path):
        print("text2")
        self.rd_widget.hide()
        self.i2t.set_results(path)


class ReadDecideWidget(QWidget):
    def __init__(self, parent: SteganoMainFrame):
        super().__init__(parent)
        self.image_label = None
        self.parent = parent
        self.initUI()

    def initUI(self):
        layout = QHBoxLayout()
        self.image_label = QLabel()
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        self.image_label.setMaximumWidth(1000)
        self.image_label.setMinimumWidth(1000)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("background:#323232;")
        pix = QPixmap()
        self.image_label.setPixmap(pix)
        layout.addWidget(self.image_label)
        ro_widget = ReadOptionsWidget(self)
        layout.addWidget(ro_widget)
        self.setLayout(layout)

    def set_image(self, path):
        pixmap = QPixmap(path)
        self.image_label.setPixmap(pixmap)

    def hide(self):
        print("read - 3")
        self.setVisible(False)
        print("read -4")

    def show(self):
        self.setVisible(True)

    def read_text(self, path):
        print("read text 1")
        self.parent.read_text(path)

    def read_image(self, path):
        print('read image 1')
        self.parent.read_image(path)

    def image_in_image(self, path):
        print('im')
        self.parent.image_in_image(path)

    def text_in_image(self, path):
        print("tex1")
        self.parent.text_in_image(path)


class ReadOptionsWidget(QFrame):
    def __init__(self, parent: ReadDecideWidget):
        super().__init__(parent)
        self.parent = parent
        self.path = None
        self.initUI()

    def initUI(self):
        self.setMinimumWidth(400)
        self.setMaximumWidth(400)
        self.setStyleSheet("background:#3a3a3a; border: 3px solid #323232;")
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        title = QLabel("Steganography")
        title.setStyleSheet("color:#aeaeae;border:none;font-size:30px; letter-spacing:1px;")
        instruction = QLabel("Load base image and chose next step")
        instruction.setStyleSheet("color:#aeaeae;font-size:17px;")
        load = QPushButton("load image")
        load.setStyleSheet("QPushButton {letter-spacing:1px; color:#9d9d9d; text-transform:uppercase; "
                           "color:#aeaeae;background:#323232;  padding-top:2px; padding-bottom:2px;"
                           "font-size:16px; letter-spacing:1px;}"
                           "QPushButton::pressed {background:#515151;}")
        load.clicked.connect(self.load_image)
        subtitle_1 = QLabel("Hide message:")
        subtitle_1.setStyleSheet("border: none; color:#aeaeae;font-size:17px;")
        subtitle_2 = QLabel("Read message:")
        subtitle_2.setStyleSheet("border: none; color:#aeaeae;font-size:17px;")
        buttons_1 = QWidget()
        l_1 = QHBoxLayout()
        button1 = QPushButton("text in image")
        button1.clicked.connect(self.text_in_image)
        button1.setStyleSheet("QPushButton {color:#9d9d9d; letter-spacing:1px; background:#414141; "
                              "text-transform:uppercase;font-size:13px; padding-top:2px; padding-bottom:2px;} "
                              "QPushButton::pressed {background:#515151;}")
        button2 = QPushButton("image in image")
        button2.setStyleSheet("QPushButton {color:#9d9d9d; letter-spacing:1px; background:#414141; "
                              "text-transform:uppercase;font-size:13px;  padding-top:2px; padding-bottom:2px;} "
                              "QPushButton::pressed {background:#515151;}")
        button2.clicked.connect(self.image_in_image)
        l_1.addWidget(button1)
        l_1.addWidget(button2)
        buttons_1.setLayout(l_1)
        buttons_2 = QWidget()
        l_2 = QHBoxLayout()
        button3 = QPushButton("read text")
        button3.clicked.connect(self.read_text)
        button3.setStyleSheet("QPushButton {color:#9d9d9d; letter-spacing:1px; background:#414141; "
                              "text-transform:uppercase;font-size:13px;  padding-top:2px; padding-bottom:2px;} "
                              "QPushButton::pressed {background:#515151;}")
        button4 = QPushButton("read image")
        button4.clicked.connect(self.read_image)
        button4.setStyleSheet("QPushButton {color:#9d9d9d; letter-spacing:1px; background:#414141; "
                              "text-transform:uppercase;font-size:13px;  padding-top:2px; padding-bottom:2px;} "
                              "QPushButton::pressed {background:#515151;}")
        l_2.addWidget(button3)
        l_2.addWidget(button4)
        buttons_2.setLayout(l_2)
        layout.addWidget(title)
        layout.addWidget(instruction)
        layout.addWidget(load)
        layout.addWidget(subtitle_1)
        layout.addWidget(buttons_1)
        layout.addWidget(subtitle_2)
        layout.addWidget(buttons_2)
        self.setLayout(layout)

    def load_image(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name = QFileDialog.getOpenFileName(self, 'Open File', '',
                                                "image Files (*.png)")
        if file_name[0] == '':
            print('error')
        elif file_name:
            self.path = file_name[0]
            self.parent.set_image(file_name[0])
        else:
            print('error')

    def text_in_image(self):
        if self.path is None:
            print("error")
            return
        print("text in image")
        self.parent.text_in_image(self.path)

    def image_in_image(self):
        if self.path is None:
            print("error 4")
            return
        print("image in image")
        self.parent.image_in_image(self.path)

    def read_text(self):
        if self.path is None:
            print("error")
            return
        print("read text")
        self.parent.read_text(self.path)

    def read_image(self):
        if self.path is None:
            print("error")
            return
        print("read image")
        self.parent.read_image(self.path)


class ReadTextWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.base_image_label = None
        self.text_label = None
        self.initUI()

    def initUI(self):
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        layout = QHBoxLayout()
        self.base_image_label = QLabel()
        self.base_image_label.setMaximumWidth(800)
        self.base_image_label.setMinimumWidth(800)
        self.base_image_label.setAlignment(Qt.AlignCenter)
        self.base_image_label.setStyleSheet("background:#323232;")
        pix = QPixmap()
        self.base_image_label.setPixmap(pix)
        layout.addWidget(self.base_image_label)
        self.text_label = QLabel()
        self.text_label.setWordWrap(True)
        self.text_label.setMaximumWidth(800)
        self.text_label.setMinimumWidth(800)
        self.text_label.setAlignment(Qt.AlignCenter)
        self.text_label.setStyleSheet("background:#323232; color:#9d9d9d; font-size:15px;")
        pix = QPixmap()
        self.text_label.setPixmap(pix)
        layout.addWidget(self.text_label)
        self.setLayout(layout)
        self.setVisible(False)

    def set_results(self, path):
        print(path)
        pixmap = QPixmap(path)
        self.base_image_label.setPixmap(pixmap)
        lsb = LSBSteganography(path)
        text = lsb.read_text()
        self.text_label.setText(text)
        self.setVisible(True)
        print(text)

    def hide(self):
        self.setVisible(False)

    def show(self):
        self.setVisible(True)


class ReadImageWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.base_image_label = None
        self.result_image_label = None
        self.initUI()

    def initUI(self):
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        layout = QHBoxLayout()
        self.base_image_label = QLabel()
        self.base_image_label.setMaximumWidth(800)
        self.base_image_label.setMinimumWidth(800)
        self.base_image_label.setAlignment(Qt.AlignCenter)
        self.base_image_label.setStyleSheet("background:#323232;")
        pix = QPixmap()
        self.base_image_label.setPixmap(pix)
        layout.addWidget(self.base_image_label)
        self.result_image_label = QLabel()
        self.result_image_label.setMaximumWidth(800)
        self.result_image_label.setMinimumWidth(800)
        self.result_image_label.setAlignment(Qt.AlignCenter)
        self.result_image_label.setStyleSheet("background:#323232;")
        pix = QPixmap()
        self.result_image_label.setPixmap(pix)
        layout.addWidget(self.result_image_label)
        self.setLayout(layout)
        self.setVisible(False)

    def set_results(self, path):
        print(path)
        pixmap = QPixmap(path)
        self.base_image_label.setPixmap(pixmap)
        lsb = LSBSteganography(path)
        image = lsb.read_image()
        pixmap = image.get_pixmap()
        self.result_image_label.setPixmap(pixmap)
        self.setVisible(True)
        print('done')

    def hide(self):
        self.setVisible(False)

    def show(self):
        self.setVisible(True)


class ImageInImageWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.base_image_label = None
        self.result_image = None
        self.hidden_image = None
        self.text_label = None
        self.hidden_path = None
        self.path = None
        self.lsb = None
        self.initUI()

    def initUI(self):
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        layout = QVBoxLayout()
        w_1 = QWidget()
        w_2 = QWidget()
        l_1 = QHBoxLayout()
        l_2 = QHBoxLayout()
        self.base_image_label = QLabel()
        self.base_image_label.setMaximumWidth(800)
        self.base_image_label.setMinimumWidth(800)
        self.base_image_label.setAlignment(Qt.AlignCenter)
        self.base_image_label.setStyleSheet("background:#323232;")
        pix = QPixmap()
        self.base_image_label.setPixmap(pix)
        l_1.addWidget(self.base_image_label)
        self.hidden_image = QLabel()
        self.hidden_image.setMaximumWidth(1200)
        self.hidden_image.setMinimumWidth(1200)
        self.hidden_image.setAlignment(Qt.AlignCenter)
        self.hidden_image.setStyleSheet("background:#323232;")
        pix = QPixmap()
        self.hidden_image.setPixmap(pix)
        l_2.addWidget(self.hidden_image)
        self.result_image = QLabel()
        self.result_image.setMaximumWidth(800)
        self.result_image.setMinimumWidth(800)
        self.result_image.setAlignment(Qt.AlignCenter)
        self.result_image.setStyleSheet("background:#323232;")
        pix = QPixmap()
        self.result_image.setPixmap(pix)
        l_1.addWidget(self.result_image)
        menu = QWidget()
        menu.setMaximumWidth(400)
        menu.setMinimumWidth(400)
        ml = QVBoxLayout()
        ml.setAlignment(Qt.AlignTop)
        si_button = QPushButton("set image")
        si_button.clicked.connect(self.set_hidden_image)
        si_button.setStyleSheet("QPushButton {color:#9d9d9d; letter-spacing:1px; background:#414141; "
                                "text-transform:uppercase;font-size:13px; padding-top:2px; padding-bottom:2px;} "
                                "QPushButton::pressed {background:#515151;}")
        hi_button = QPushButton("hide image")
        hi_button.clicked.connect(self.hide_image)
        hi_button.setStyleSheet("QPushButton {color:#9d9d9d; letter-spacing:1px; background:#414141; "
                                "text-transform:uppercase;font-size:13px; padding-top:2px; padding-bottom:2px;} "
                                "QPushButton::pressed {background:#515151;}")
        svi_button = QPushButton("save image")
        svi_button.clicked.connect(self.save_image)
        svi_button.setStyleSheet("QPushButton {color:#9d9d9d; letter-spacing:1px; background:#414141; "
                                "text-transform:uppercase;font-size:13px; padding-top:2px; padding-bottom:2px;} "
                                "QPushButton::pressed {background:#515151;}")
        ml.addWidget(si_button)
        ml.addWidget(hi_button)
        ml.addWidget(svi_button)
        menu.setLayout(ml)
        l_2.addWidget(menu)
        w_1.setLayout(l_1)
        w_2.setLayout(l_2)
        layout.addWidget(w_1)
        layout.addWidget(w_2)
        layout.addWidget(self.text_label)
        self.setLayout(layout)
        self.setVisible(False)

    def set_results(self, path):
        self.path = path
        print(path)
        pixmap = QPixmap(path)
        self.base_image_label.setPixmap(pixmap)
        self.setVisible(True)

    def set_hidden_image(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name = QFileDialog.getOpenFileName(self, 'Open File', '',
                                                "image Files (*.png)")
        if file_name[0] == '':
            print('error')
        elif file_name:
            self.hidden_path = file_name[0]
            pixmap = QPixmap(self.hidden_path)
            self.hidden_image.setPixmap(pixmap)
        else:
            print('error')

    def hide_image(self):
        self.lsb = LSBSteganography(self.path)
        self.lsb.hide_image(self.hidden_path)
        pixmap = self.lsb.image.get_pixmap()
        self.result_image.setPixmap(pixmap)

    def save_image(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name = QFileDialog.getSaveFileName(self, 'Open File', '',
                                                "image Files (*.png)")
        if file_name[0] == '':
            print('error')
        elif file_name:
            self.lsb.save_image(file_name[0])
        else:
            print('error')

    def hide(self):
        self.setVisible(False)

    def show(self):
        self.setVisible(True)


class TextInImageWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.base_image_label = None
        self.result_image = None
        self.hidden_text = None
        self.text_label = None
        self.hidden_path = None
        self.path = None
        self.lsb = None
        self.h_text = None
        self.initUI()

    def initUI(self):
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        layout = QVBoxLayout()
        w_1 = QWidget()
        w_2 = QWidget()
        l_1 = QHBoxLayout()
        l_2 = QHBoxLayout()
        self.base_image_label = QLabel()
        self.base_image_label.setMaximumWidth(800)
        self.base_image_label.setMinimumWidth(800)
        self.base_image_label.setAlignment(Qt.AlignCenter)
        self.base_image_label.setStyleSheet("background:#323232;")
        pix = QPixmap()
        self.base_image_label.setPixmap(pix)
        l_1.addWidget(self.base_image_label)
        self.hidden_text = QLabel()
        self.hidden_text.setWordWrap(True)
        self.hidden_text.setMaximumWidth(1200)
        self.hidden_text.setMinimumWidth(1200)
        self.hidden_text.setAlignment(Qt.AlignCenter)
        self.hidden_text.setStyleSheet("background:#323232;color:#9d9d9d; font-size:15px;")
        pix = QPixmap()
        self.hidden_text.setPixmap(pix)
        l_2.addWidget(self.hidden_text)
        self.result_image = QLabel()
        self.result_image.setMaximumWidth(800)
        self.result_image.setMinimumWidth(800)
        self.result_image.setAlignment(Qt.AlignCenter)
        self.result_image.setStyleSheet("background:#323232;")
        pix = QPixmap()
        self.result_image.setPixmap(pix)
        l_1.addWidget(self.result_image)
        menu = QWidget()
        menu.setMaximumWidth(400)
        menu.setMinimumWidth(400)
        ml = QVBoxLayout()
        ml.setAlignment(Qt.AlignTop)
        si_button = QPushButton("set text")
        si_button.clicked.connect(self.set_hidden_text)
        si_button.setStyleSheet("QPushButton {color:#9d9d9d; letter-spacing:1px; background:#414141; "
                                "text-transform:uppercase;font-size:13px; padding-top:2px; padding-bottom:2px;} "
                                "QPushButton::pressed {background:#515151;}")
        hi_button = QPushButton("hide text")
        hi_button.clicked.connect(self.hide_text)
        hi_button.setStyleSheet("QPushButton {color:#9d9d9d; letter-spacing:1px; background:#414141; "
                                "text-transform:uppercase;font-size:13px; padding-top:2px; padding-bottom:2px;} "
                                "QPushButton::pressed {background:#515151;}")
        svi_button = QPushButton("save image")
        svi_button.clicked.connect(self.save_image)
        svi_button.setStyleSheet("QPushButton {color:#9d9d9d; letter-spacing:1px; background:#414141; "
                                 "text-transform:uppercase;font-size:13px; padding-top:2px; padding-bottom:2px;} "
                                 "QPushButton::pressed {background:#515151;}")
        ml.addWidget(si_button)
        ml.addWidget(hi_button)
        ml.addWidget(svi_button)
        menu.setLayout(ml)
        l_2.addWidget(menu)
        w_1.setLayout(l_1)
        w_2.setLayout(l_2)
        layout.addWidget(w_1)
        layout.addWidget(w_2)
        layout.addWidget(self.text_label)
        self.setLayout(layout)
        self.setVisible(False)

    def set_results(self, path):
        self.path = path
        print(path)
        pixmap = QPixmap(path)
        self.base_image_label.setPixmap(pixmap)
        self.setVisible(True)

    def set_hidden_text(self):
        print('set_text')
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name = QFileDialog.getOpenFileName(self, 'Open File', '',
                                                "Text Files (*.txt)")
        if file_name[0] == '':
            print('error - 3')
        elif file_name:
            print(file_name[0])
            self.hidden_path = file_name[0]
            with open(self.hidden_path) as f:
                self.h_text = f.readlines()
                print(self.h_text[0])
                self.hidden_text.setText(self.h_text[0])
        else:
            print('error - 6')

    def hide_text(self):
        self.lsb = LSBSteganography(self.path)
        self.lsb.load_text(self.h_text[0])
        self.lsb.hide_text()
        pixmap = self.lsb.image.get_pixmap()
        self.result_image.setPixmap(pixmap)

    def save_image(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name = QFileDialog.getSaveFileName(self, 'Open File', '',
                                                "image Files (*.png)")
        if file_name[0] == '':
            print('error')
        elif file_name:
            self.lsb.save_image(file_name[0])
        else:
            print('error')

    def hide(self):
        self.setVisible(False)

    def show(self):
        self.setVisible(True)
