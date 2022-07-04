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
        self.hidden_image = CImage()
        self.max_length = self.image.width * self.image.height * 3

    def load_text(self, text):
        self.text = text
        self.binary_text = self.BD.text_to_binary(text)

    def save_image(self, path):
        self.image.save_image(path)

    def full_text(self):
        binary_text_length = len(self.binary_text)
        if binary_text_length < self.max_length:
            n = self.max_length // binary_text_length
            new_text = n * self.binary_text
            l = self.max_length - len(new_text) - 1
            new_text += self.binary_text[:l - 3]
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
                else:
                    val_b = self.BD.number_to_binary(val)
                    val_str = val_b[:7] + self.binary_text[index]
                    new_val = self.BD.binary_to_number(val_str)
                    val[...] = new_val
                    index += 1
        self.image.update_image()

    def hide_image(self, image_path, o="simple"):
        hidden = CImage()
        hidden.read_image(image_path)
        message = self.BD.image_to_binary(hidden)
        if len(message) > self.max_length:
            print("Image to big")
            return
        matrix = self.image.image_matrix
        l = len(message)
        index = 0
        with np.nditer(matrix, op_flags=['readwrite']) as it:
            for val in it:
                if index == l:
                    break
                else:
                    val_b = self.BD.number_to_binary(val)
                    val_str = val_b[:7] + message[index]
                    new_val = self.BD.binary_to_number(val_str)
                    val[...] = new_val
                    index += 1
        self.image.update_image()

    def read_text(self):
        matrix = self.image.image_matrix
        btext = ""
        end_sign = 0
        index = 0
        with np.nditer(matrix, op_flags=['readwrite']) as it:
            for i, val in enumerate(it):
                if end_sign == 3:
                    break
                else:
                    val_b = self.BD.number_to_binary(val)
                    btext += val_b[7]
                    if index % 9 == 8:
                        if self.BD.binary_to_text(btext[-9:]) == "#":
                            end_sign += 1
                    index += 1
        rtext = self.BD.binary_to_text(btext)
        rtext = rtext[:len(rtext) - 3]
        return rtext

    def read_image(self):
        matrix = self.image.image_matrix
        btext = ""
        with np.nditer(matrix, op_flags=['readwrite']) as it:
            for i, val in enumerate(it):
                val_b = self.BD.number_to_binary(val)
                btext += val_b[7]
        im = self.BD.binary_to_image(btext)
        return im


lsb = LSBSteganography(r"C:\Users\jbtok\Desktop\studia_szkola\studia\semestr6\praca\vCryptography\vCryptography"
                       r"\images\ex1.png")
lsb.load_text("Zażółć gęślą jaźń")
lsb.hide_text("simple")
lsb.save_image(r"C:\Users\jbtok\Desktop\studia_szkola\studia\semestr6\praca\vCryptography"
               r"\vCryptography\images\ex2.png")

lsb1 = LSBSteganography(r"C:\Users\jbtok\Desktop\studia_szkola\studia\semestr6\praca\vCryptography\vCryptography"
                        r"\images\ex2.png")
print(lsb1.read_text())

lsb2 = LSBSteganography(r"C:\Users\jbtok\Desktop\studia_szkola\studia\semestr6\praca\vCryptography\vCryptography"
                        r"\images\ex1.png")
lsb2.hide_image(r"C:\Users\jbtok\Desktop\studia_szkola\studia\semestr6\praca\vCryptography\vCryptography"
                r"\images\im1.png")
lsb2.save_image(r"C:\Users\jbtok\Desktop\studia_szkola\studia\semestr6\praca\vCryptography\vCryptography"
                r"\images\ex3.png")
lsb3 = LSBSteganography(r"C:\Users\jbtok\Desktop\studia_szkola\studia\semestr6\praca\vCryptography\vCryptography"
                        r"\images\ex3.png")
im = lsb3.read_image()
im.show_image()