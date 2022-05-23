import numpy as np

from utils.BinaryData import BinaryData
from utils.Image import CImage


class LSBSteganography:
    def __init__(self, image_path, text):
        self.BD = BinaryData()
        self.image = CImage()
        self.image.read_image(image_path)
        self.text = text
        self.binary_text = self.BD.text_to_binary(text)
        print(self.binary_text)

    def hide_text(self):
        matrix = self.image.image_matrix
        l = len(self.binary_text)
        index = 0
        with np.nditer(matrix, op_flags=['readwrite']) as it:
            for i, val in enumerate(it):
                if index == l:
                    break
                if i % 4 != 3:
                    val_b = self.BD.number_to_binary(val)
                    val_str = val_b[:7] + self.binary_text[index]
                    new_val = self.BD.binary_to_number(val_str)
                    val[...] = new_val
                    index += 1
        self.image.update_image()
        self.image.show_image()
        self.image.save_image(r"C:\Users\jbtok\Desktop\ex2.png")

    def read_text(self):
        matrix = self.image.image_matrix
        btext = ""
        with np.nditer(matrix, op_flags=['readwrite']) as it:
            for i, val in enumerate(it):
                if i % 4 != 3:
                    val_b = self.BD.number_to_binary(val)
                    btext += val_b[7]
        print(btext)
        rtext = self.BD.binary_to_text(btext)
        print(rtext)


lsb = LSBSteganography(r"C:\Users\jbtok\Desktop\ex1.png", "Zażółć gęślą jaźń")
lsb.hide_text()
lsb.read_text()
