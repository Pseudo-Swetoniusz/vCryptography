import numpy as np
from PIL import Image
from utils.Image import CImage


class BinaryImage:
    def __init__(self):
        self.original_image = None
        self.binary_image = None
        self.width = None
        self.height = None
        self.histogram = [0]*256

    def load_image(self, img: CImage):
        self.original_image = img
        self.width = img.get_width()
        self.height = img.get_height()

    def create_histogram(self):
        matrix = self.original_image.image_matrix
        if self.original_image.mode == "RGB" or self.original_image.mode == "RGBA":
            with np.nditer(matrix, op_flags=['readwrite']) as it:
                for i, val in enumerate(it):
                    y = int(0.2126 * val[0] + 0.7152 * val[1] + 0.0722 * val[2])
                    self.histogram[y] += 1
        else:
            with np.nditer(matrix, op_flags=['readwrite']) as it:
                for i, val in enumerate(it):
                    self.histogram[val] += 1
        return self.histogram

    def get_histogram(self):
        return self.histogram
