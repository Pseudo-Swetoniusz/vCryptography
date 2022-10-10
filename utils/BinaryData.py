import string
import numpy as np
from utils import Image
from utils.Image import CImage


class BinaryData:
    def image_to_binary(self, image: Image.CImage):
        matrix = image.image_matrix
        result = format(image.width, '012b') + format(image.height, '012b')
        with np.nditer(matrix, op_flags=['readwrite']) as it:
            for val in it:
                val_b = self.number_to_binary(val)
                result += str(val_b)
        return result

    def binary_to_image(self, binary: string):
        wb = binary[:12]
        width = int(wb, 2)
        hb = binary[12:24]
        height = int(hb, 2)
        C = CImage()
        im_array = [[[] for _ in range(width)] for _ in range(height)]
        index = 24
        for h in range(height):
            for w in range(width):
                r = int(binary[index:index + 8], 2)
                g = int(binary[index + 8:index + 16], 2)
                b = int(binary[index + 16:index + 24], 2)
                a = im_array[h][w]
                a.append(r)
                a.append(g)
                a.append(b)
                index = index + 24
        im_array = np.array(im_array)
        C.update_matrix(im_array.astype(np.uint8))
        C.update_image()
        C.set_image()
        return C

    def text_to_binary(self, text: string):
        text_bin = ""
        for l in text:
            t = format(ord(l), '09b')
            text_bin += t
        return text_bin

    def binary_to_text(self, binary: string):
        text = ""
        for i in range(0, len(binary), 9):
            bl = binary[i:i + 9]
            l = chr(int(bl, 2))
            text += l
        return text

    def number_to_binary(self, number: int):
        return format(number, '08b')

    def binary_to_number(self, binary: string):
        return int(binary, 2)
