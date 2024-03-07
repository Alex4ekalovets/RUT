import cv2
import numpy as np
from numpy import ndarray


def nothing(args): pass


cv2.namedWindow("setup")
cv2.namedWindow("setup2")
cv2.createTrackbar("b1", "setup", 0, 255, nothing)
cv2.createTrackbar("g1", "setup", 0, 255, nothing)
cv2.createTrackbar("r1", "setup", 0, 255, nothing)
cv2.createTrackbar("b2", "setup", 255, 255, nothing)
cv2.createTrackbar("g2", "setup", 255, 255, nothing)
cv2.createTrackbar("r2", "setup", 255, 255, nothing)
cv2.createTrackbar("blur", "setup2", 0, 10, nothing)
cv2.createTrackbar("angle", "setup2", 0, 360, nothing)
cv2.createTrackbar("size", "setup2", 100, 1000, nothing)

fn = "test_data/2.jpg"  # путь к файлу с картинкой
img = cv2.imread(fn)  # загрузка изображения
percent = 50
width = img.shape[1]
height = img.shape[0]
cv2.createTrackbar("crop top", "setup2", 0, height, nothing)
cv2.createTrackbar("crop right", "setup2", width, width, nothing)
cv2.createTrackbar("crop bottom", "setup2", height, height, nothing)
cv2.createTrackbar("crop left", "setup2", 0, width, nothing)

while True:
    r1 = cv2.getTrackbarPos('r1', 'setup')
    g1 = cv2.getTrackbarPos('g1', 'setup')
    b1 = cv2.getTrackbarPos('b1', 'setup')
    r2 = cv2.getTrackbarPos('r2', 'setup')
    g2 = cv2.getTrackbarPos('g2', 'setup')
    b2 = cv2.getTrackbarPos('b2', 'setup')
    blur = cv2.getTrackbarPos('blur', 'setup2')
    angle = cv2.getTrackbarPos('angle', 'setup2')
    size = cv2.getTrackbarPos('size', 'setup2')
    crop_top = cv2.getTrackbarPos('crop top', 'setup2')
    crop_right = cv2.getTrackbarPos('crop right', 'setup2')
    crop_bottom = cv2.getTrackbarPos('crop bottom', 'setup2')
    crop_left = cv2.getTrackbarPos('crop left', 'setup2')
    min_p = (g1, b1, r1)
    max_p = (g2, b2, r2)
      # сглаживание изображения
    img_mask = cv2.inRange(img_bl, min_p, max_p)
    img_m = cv2.bitwise_and(img, img, mask=img_mask)

    cv2.imshow('image', result)
    if cv2.waitKey(33) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()


def image_handler(image: str | ndarray, **kwargs) -> ndarray:
    if isinstance(image, str):
        image = cv2.imread(image)
    elif not isinstance(image, ndarray):
        raise TypeError("Передайте путь к изображению в виде строки или изображение в виде numpy массива")

    default_height, default_width, _ = image.shape

    if 'rotate' in kwargs:
        image_center = tuple(np.array(image.shape[1::-1]) / 2)
        rot_mat = cv2.getRotationMatrix2D(image_center, kwargs['rotate'], 1.0)
        image = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)

    if 'crop' in kwargs:
        top, bottom, left, right = map(int, kwargs['crop'])
        image = image[top:bottom, left:right]

    if 'resize' in kwargs:
        image = cv2.resize(src=image, dsize=(0, 0), fx=size / 100, fy=size / 100)

    if 'blur' in kwargs:
        image = cv2.medianBlur(image, 1 + blur * 2)

    if 'gray' in kwargs:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    return image


def convert_image_to_bytes(image: ndarray) -> bytes:
    ret, image = cv2.imencode('.jpg', image)
    image = image.tobytes()
    return image


if __name__ == "__main__":
    pass
