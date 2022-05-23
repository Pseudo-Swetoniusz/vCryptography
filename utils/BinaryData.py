class BinaryData:
    def text_to_binary(self, text):
        text_bin = ""
        for l in text:
            t = format(ord(l), '09b')
            text_bin += t
        return text_bin

    def binary_to_text(self, binary):
        text = ""
        for i in range(0, len(binary), 9):
            bl = binary[i:i + 9]
            l = chr(int(bl, 2))
            text += l
        return text

    def number_to_binary(self, number):
        return format(number, '08b')

    def binary_to_number(self, binary):
        return int(binary, 2)
