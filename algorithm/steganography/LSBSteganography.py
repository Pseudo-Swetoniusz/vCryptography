import numpy as np

from utils.BinaryData import BinaryData
from utils.Image import CImage


class LSBSteganography:
    def __init__(self, image_path):
        self.BD = BinaryData()
        self.image = CImage()
        self.image.read_image(image_path)
        self.text = None
        self.binary_text = None
        self.max_length = self.image.width * self.image.height * 3

    def load_text(self, text):
        self.text = text
        self.binary_text = self.BD.text_to_binary(text)

    def full_text(self):
        binary_text_length = len(self.binary_text)
        if binary_text_length < self.max_length:
            n = self.max_length // binary_text_length
            new_text = n * self.binary_text
            l = self.max_length - len(new_text) - 1
            new_text += self.binary_text[:l-3]
            new_text += "###"
            self.binary_text = new_text

    def hide_text(self, o="simple"):
        if o == "full":
            self.full_text()
        else:
            self.text += "###"
            self.binary_text = self.BD.text_to_binary(self.text)
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
        self.image.save_image(r"C:\Users\jbtok\Desktop\studia_szkola\studia\semestr6\praca\vCryptography"
                              r"\vCryptography\images\ex2.png")

    def read_text(self):
        matrix = self.image.image_matrix
        btext = ""
        end_sign = 0
        index = 0
        with np.nditer(matrix, op_flags=['readwrite']) as it:
            for i, val in enumerate(it):
                if end_sign == 3:
                    break
                if i % 4 != 3:
                    val_b = self.BD.number_to_binary(val)
                    btext += val_b[7]
                    if index % 9 == 8:
                        if self.BD.binary_to_text(btext[-9:]) == "#":
                            end_sign += 1
                    index += 1
        rtext = self.BD.binary_to_text(btext)
        rtext = rtext[:len(rtext)-3]
        print(rtext)


lsb = LSBSteganography(r"C:\Users\jbtok\Desktop\studia_szkola\studia\semestr6\praca\vCryptography\vCryptography"
                       r"\images\ex1.png")
lsb.load_text("Zażółć gęślą jaźń")
lsb.hide_text("full")

lsb = LSBSteganography(r"C:\Users\jbtok\Desktop\studia_szkola\studia\semestr6\praca\vCryptography\vCryptography"
                       r"\images\ex2.png")
lsb.read_text()
