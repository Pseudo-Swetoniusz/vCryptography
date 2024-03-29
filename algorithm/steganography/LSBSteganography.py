import numpy as np
import time

from utils.BinaryData import BinaryData
from utils.Image import CImage


class ImageTooBigException(Exception):
    def __init__(self, *args):
        super().__init__(args)

    def __str__(self):
        return "Image is too big to hide."


class TextTooLongException(Exception):
    def __init__(self, *args):
        super().__init__(args)

    def __str__(self):
        return "Text is too long to hide."


class LSBSteganography:
    def __init__(self):
        self.BD = BinaryData()
        self.image = CImage()
        self.text = None
        self.binary_text = None
        self.hidden_image = CImage()
        self.max_length = None

    def load_image(self, image_path):
        self.image.read_image(image_path)
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
            new_text += "#####"
            self.binary_text = new_text

    def hide_text(self, o="simple"):
        if o == "full":
            self.full_text()
        else:
            self.text += "#####"
            self.binary_text = self.BD.text_to_binary(self.text)
        matrix = self.image.image_matrix
        l = len(self.binary_text)
        if l > self.max_length:
            raise TextTooLongException()
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
            raise ImageTooBigException()
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
                if end_sign == 5:
                    break
                else:
                    val_b = self.BD.number_to_binary(val)
                    btext += val_b[7]
                    if index % 8 == 7:
                        if self.BD.binary_to_text(btext[-8:]) == "#":
                            end_sign += 1
                    index += 1
        rtext = self.BD.binary_to_text(btext)
        rtext = rtext[:len(rtext) - 5]
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

    def hide_binary_image(self, bimg):
        message = self.BD.binary_image_to_binary(bimg)
        if len(message) > self.max_length:
            raise ImageTooBigException()
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

    def read_binary_image(self):
        matrix = self.image.image_matrix
        btext = ""
        with np.nditer(matrix, op_flags=['readwrite']) as it:
            for i, val in enumerate(it):
                val_b = self.BD.number_to_binary(val)
                btext += val_b[7]
        im = self.BD.binary_to_binary_image(btext)
        return im
