import os
import pytest
from utils.BinaryData import BinaryData
from utils.Image import CImage


@pytest.fixture
def binary_data():
    return BinaryData()


@pytest.fixture
def root():
    return os.path.abspath(os.curdir)


def test_image_to_binary(binary_data, root):
    c_image = CImage()
    c_image.read_image(os.path.join(root, "resources/img.png"))
    binary = binary_data.image_to_binary(c_image)
    test_binary = ""
    with open(os.path.join(root, "resources/test_binary"), 'r') as file:
        test_binary = file.read().replace('\n', '')
    assert binary == test_binary


def test_binary_to_image(binary_data, root):
    test_binary = ""
    with open(os.path.join(root, "resources/test_binary"), 'r') as file:
        test_binary = file.read().replace('\n', '')
    image = binary_data.binary_to_image(test_binary)
    image.show_image()
    test_image = CImage()
    test_image.read_image(os.path.join(root, "resources/img.png"))
    assert image.compare_image(test_image) is True


def test_text_to_binary(binary_data):
    test_text = "Zażółć gęślą jaźń"
    binary = binary_data.text_to_binary(test_text)
    assert binary == "0010110100011000011011111000111100111010000101000001110001000000011001111000110011010110110011" \
                     "01100100000101000100000001101010001100001101111010101000100"


def test_binary_to_test(binary_data):
    test_binary = "0010110100011000011011111000111100111010000101000001110001000000011001111000110011010110110011011" \
                  "00100000101000100000001101010001100001101111010101000100"
    text = binary_data.binary_to_text(test_binary)
    assert text == "Zażółć gęślą jaźń"


def test_number_to_binary(binary_data):
    test_number = 220
    binary = binary_data.number_to_binary(test_number)
    assert binary == "11011100"


def test_binary_to_number(binary_data):
    test_binary = "11011100"
    number = binary_data.binary_to_number(test_binary)
    assert number == 220