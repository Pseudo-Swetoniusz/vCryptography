import os
import pytest
from utils.BinaryData import BinaryData
from utils.BinaryImage import BinaryImage
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


def test_binary_image_to_binary(binary_data, root):
    cimg = CImage()
    cimg.read_image(os.path.join(root, "resources/img.png"))
    bimg = BinaryImage()
    bimg.load_image(cimg)
    bimg.create_histogram()
    t = bimg.otsu()
    bimg.get_binary_image(t)
    new_binary = binary_data.binary_image_to_binary(bimg)
    with open(os.path.join(root, "resources/test_binary_2"), 'r') as file:
        test_binary = file.read().replace('\n', '')
    assert new_binary == test_binary


def test_binary_to_binary_image(binary_data, root):
    with open(os.path.join(root, "resources/test_binary_2"), 'r') as file:
        test_binary = file.read().replace('\n', '')
    bimg = binary_data.binary_to_binary_image(test_binary)
    bimg.show_image()
    test_image = CImage()
    test_image.read_image(os.path.join(root, "resources/img_2.png"))
    assert test_image.compare_image(bimg)

def test_text_to_binary(binary_data):
    test_text = "Zażółć gęślą jaźń"
    binary = binary_data.text_to_binary(test_text)
    assert binary == "0101101001100001110001011011110011000011101100111100010110000010110001001000011100100000011001111100010010011001110001011001101101101100110001001000010100100000011010100110000111000101101110101100010110000100"


def test_binary_to_test(binary_data):
    test_binary = "0101101001100001110001011011110011000011101100111100010110000010110001001000011100100000011001111100010010011001110001011001101101101100110001001000010100100000011010100110000111000101101110101100010110000100"
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
