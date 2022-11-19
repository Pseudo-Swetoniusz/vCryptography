import numpy as np
from PIL import Image
from utils.Image import CImage


class BinaryImage(CImage):
    def __init__(self):
        super(BinaryImage, self).__init__()
        self.histogram = np.array([0] * 256)

    def load_image(self, img: CImage):
        self.original_image = img.original_image
        self.new_image = img.new_image
        self.width = img.get_width()
        self.height = img.get_height()
        self.image_matrix = img.image_matrix
        self.mode = img.mode

    def rgb_to_grayscale(self, r: int, g: int, b: int):
        return int(0.2126 * r + 0.7152 * g + 0.0722 * b)

    def create_histogram(self):
        matrix = self.image_matrix
        if self.mode == "RGB" or self.mode == "RGBA":
            for x in matrix:
                for y in x:
                    val = int(self.rgb_to_grayscale(y[0], y[1], y[2]))
                    self.histogram[val] += 1
        else:
            for x in matrix:
                for y in x:
                    self.histogram[y] += 1
        return np.array(self.histogram)

    def get_histogram(self):
        return self.histogram

    def otsu(self):
        def calculate_hist_mean(a, b):
            sum = 0
            num = 0
            for i in range(a, b):
                sum += self.histogram[i] * i
                num += self.histogram[i]
            if num == 0:
                return 0
            return sum / num

        def calculate_hist_variance(a, b):
            mean = calculate_hist_mean(a, b)
            num = 0
            sum = 0
            for i in range(a, b):
                num += self.histogram[i]
                sum += self.histogram[i] * (i - mean) * (i - mean)
            if num == 0:
                return 0
            return sum / num

        def weight(a, b):
            sum = 0
            for i in range(a, b):
                sum += self.histogram[i]
            return sum / (self.width * self.height)

        def withinClassVariance(t):
            back_var = calculate_hist_variance(0, t)
            fore_var = calculate_hist_variance(t, 256)
            back_weight = weight(0, t)
            fore_weight = weight(t, 256)
            return back_var * back_weight + fore_var * fore_weight

        minVar = withinClassVariance(0)
        threshold = 0
        for i in range(1, 256):
            var = withinClassVariance(i)
            if var < minVar:
                minVar = var
                threshold = i
        return threshold

    def get_binary_image(self, k: int):
        old_matrix = self.image_matrix
        width = self.get_width()
        height = self.get_height()
        new_matrix = [[0 for _ in range(width)] for _ in range(height)]
        for y in range(height):
            for x in range(width):
                if self.rgb_to_grayscale(old_matrix[y][x][0], old_matrix[y][x][1], old_matrix[y][x][2]) > k:
                    new_matrix[y][x] = 255
                else:
                    new_matrix[y][x] = 0
        self.update_matrix(np.array(new_matrix))
        self.update_image()
        return np.array(new_matrix)

