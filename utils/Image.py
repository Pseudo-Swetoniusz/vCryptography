from PIL import Image
import numpy as np
from PyQt5.QtGui import QImage, QPixmap


class CImage:
    def __init__(self):
        self.original_image = None
        self.new_image = None
        self.image_matrix = None
        self.width = None
        self.height = None
        self.mode = None

    def read_image(self, file_path):
        self.original_image = Image.open(file_path)
        self.mode = self.original_image.mode
        self.width, self.height = self.original_image.size
        self.image_matrix = np.array(self.original_image)
        self.update_image()

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def update_matrix(self, array):
        self.image_matrix = array

    def update_image(self):
        self.new_image = Image.fromarray(self.image_matrix)
        self.mode = self.new_image.mode

    def set_image(self):
        self.original_image = Image.fromarray(self.image_matrix)
        self.width, self.height = self.original_image.size

    def save_image(self, file_path):
        self.update_image()
        self.new_image.save(file_path)

    def show_image(self):
        self.new_image.show()

    def get_pixmap(self):
        im = self.new_image
        if im.mode == "RGB":
            r, g, b = im.split()
            im = Image.merge("RGB", (b, g, r))
        elif im.mode == "RGBA":
            r, g, b, a = im.split()
            im = Image.merge("RGBA", (b, g, r, a))
        elif im.mode == "L":
            im = im.convert("RGBA")
        im2 = im.convert("RGBA")
        data = im2.tobytes("raw", "RGBA")
        qim = QImage(data, im.size[0], im.size[1], QImage.Format_ARGB32)
        pixmap = QPixmap.fromImage(qim)
        return pixmap

    def compare_image(self, img):
        if self.width != img.get_width() or self.height != img.get_height():
            return False
        else:
            for x in range(self.height):
                for y in range(self.width):
                    if not np.array_equal(self.image_matrix[x][y], img.__getitem__((x, y))):
                        return False
            return True

    def __getitem__(self, idx):
        i, j = idx
        return self.image_matrix[i][j]
