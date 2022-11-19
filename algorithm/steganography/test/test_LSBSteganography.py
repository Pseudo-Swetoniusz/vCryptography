import os
import pytest
from algorithm.steganography.LSBSteganography import LSBSteganography
from utils.BinaryImage import BinaryImage
from utils.Image import CImage


@pytest.fixture
def root():
    return os.path.abspath(os.curdir)


def test_load_image(root):
    stegano = LSBSteganography()
    test_img_path = os.path.join(root, "resources/img.png")
    stegano.load_image(test_img_path)
    assert stegano.max_length == 67500


def test_load_text():
    stegano = LSBSteganography()
    stegano.load_text("Zażółć gęślą jaźń")
    assert stegano.text == "Zażółć gęślą jaźń"
    assert stegano.binary_text == "0010110100011000011011111000111100111010000101000001110001000000011001111000110011" \
                                  "01011011001101100100000101000100000001101010001100001101111010101000100"


def test_hide_read_text(root):
    stegano = LSBSteganography()
    test_img_path = os.path.join(root, "resources/img.png")
    stegano.load_image(test_img_path)
    stegano.load_text("Zażółć gęślą jaźń")
    stegano.hide_text()
    text = stegano.read_text()
    assert text == "Zażółć gęślą jaźń"


def test_hide_read_image(root):
    stegano = LSBSteganography()
    test_image_path_1 = os.path.join(root, "resources/ex1.png")
    test_img_path_2 = os.path.join(root, "resources/img.png")
    test_img = CImage()
    test_img.read_image(test_img_path_2)
    stegano.load_image(test_image_path_1)
    stegano.hide_image(test_img_path_2)
    img = stegano.read_image()
    assert img.compare_image(test_img) is True

def test_hide_read_binary_image(root):
    stegano = LSBSteganography()
    test_image_path_1 = os.path.join(root, "resources/ex1.png")
    test_img_path_2 = os.path.join(root, "resources/img.png")
    test_img = CImage()
    test_img.read_image(test_img_path_2)
    bimg = BinaryImage()
    bimg.load_image(test_img)
    bimg.create_histogram()
    t = bimg.otsu()
    bimg.get_binary_image(t)
    stegano.load_image(test_image_path_1)
    stegano.hide_binary_image(bimg)
    img = stegano.read_binary_image()
    assert img.compare_image(bimg) is True
