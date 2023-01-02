import string
import numpy as np
from utils import Image
from utils.BinaryImage import BinaryImage
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
        im_array = [[[0, 0, 0] for _ in range(width)] for _ in range(height)]
        index = 24
        for h in range(height):
            for w in range(width):
                r = int(binary[index:index + 8], 2)
                g = int(binary[index + 8:index + 16], 2)
                b = int(binary[index + 16:index + 24], 2)
                a = im_array[h][w]
                a[0] = r
                a[1] = g
                a[2] = b
                index = index + 24
                if index >= len(binary):
                    break
            if index >= len(binary):
                break
        im_array = np.array(im_array)
        C.update_matrix(im_array.astype(np.uint8))
        C.update_image()
        C.set_image()
        return C

    def binary_image_to_binary(self, image: BinaryImage):
        matrix = image.image_matrix // 255
        result = format(image.width, '012b') + format(image.height, '012b')
        with np.nditer(matrix, op_flags=['readwrite']) as it:
            for val in it:
                result += str(val)
        return result

    def binary_to_binary_image(self, binary: string):
        wb = binary[:12]
        width = int(wb, 2)
        hb = binary[12:24]
        height = int(hb, 2)
        B = BinaryImage()
        im_array = [[0 for _ in range(width)] for _ in range(height)]
        index = 24
        for h in range(height):
            for w in range(width):
                im_array[h][w] = int(binary[index])
                index += 1
                if index >= len(binary):
                    break
            if index >= len(binary):
                break
        im_array = np.array(im_array)
        im_array = im_array * 255
        B.update_matrix(im_array)
        B.update_image()
        B.set_image()
        return B

    def text_to_binary(self, text: string):
        text_bin = ""
        text_bytes = text.encode(encoding='utf-8')
        #for l in text:
        #    t = format(ord(l), '09b')
        #    text_bin += t
        for t in text_bytes:
            text_bin += format(t, '08b')
        return text_bin

    def binary_to_text(self, binary: string):
        text = ""
        b_array = bytearray()
        #for i in range(0, len(binary), 9):
        #    bl = binary[i:i + 9]
        #    l = chr(int(bl, 2))
        #    text += l
        for i in range(0,len(binary), 8):
            byte = binary[i:i+8]
            b = int(byte,2).to_bytes(1,'big')
            b_array.append(b[0])
        try:
            text = b_array.decode(encoding='utf-8')
        except UnicodeDecodeError:
            return ''
        return text

    def number_to_binary(self, number: int):
        return format(number, '08b')

    def binary_to_number(self, binary: string):
        return int(binary, 2)
