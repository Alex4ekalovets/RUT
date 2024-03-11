import cv2
import numpy as np
import pytest

from utils.image_tools import image_handler


def test_image_handler_resize_pass():
    file = r".\tests\data\image_handler_resize_test_image.jpg"
    params = {
        "resize": {
            "width": 1000,
            "height": 2000,
            "save_ratio": False,
            "side": ""
        },
    }
    assert image_handler(file, **params).shape[:2] == (2000, 1000)


def test_image_handler_resize_fail():
    with pytest.raises(cv2.error):
        file = r".\tests\data\image_handler_resize_test_image.jpg"
        params = {
            "resize": {
                "width": -1000,
                "height": 2000,
                "save_ratio": False,
                "side": ""
            },
        }
        image_handler(file, **params)


def test_image_handler_rotate_pass():
    file = r".\tests\data\image_handler_angle_test_image.jpg"
    params = {
        "rotate": {
            "angle": 90,
        },
    }
    assert image_handler(file, **params).shape[:2] == (1556, 875)


def test_image_handler_rgb_pass():
    file = r".\tests\data\image_handler_rgb_test_image.jpg"
    params = {
        "rgb": {
            "red": 10,
            "green": 100,
            "blue": -11
        }
    }
    b, g, r = cv2.split(image_handler(file, **params))
    assert np.all(b == 0) and np.all(g == 200) and np.all(r == 255)


def test_image_handler_crop_pass():
    file = r".\tests\data\image_handler_crop_test_image.jpg"
    params = {
        "crop": {
            "top": 10,
            "bottom": 10,
            "left": 10,
            "right": 10
        },
    }
    assert image_handler(file, **params).shape[:2] == (77, 353)
