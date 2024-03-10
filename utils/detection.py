import logging
import os

from imutils import paths
from numpy import ndarray
import settings

import cv2

logger = logging.getLogger("logger")

cv2_base_dir = os.path.dirname(os.path.abspath(cv2.__file__))
haar_face_model = os.path.join(cv2_base_dir, 'data/haarcascade_frontalface_alt.xml')


class Detector:
    """Класс обнаружения объектов на изображениях"""

    def __init__(self, model: str, use_cuda: bool = False):
        self.model = model
        self.cuda = use_cuda

    def images_handler(self, path: str) -> list[ndarray]:
        """
        Обработка всех изображений из указанной директории
        :param path: Путь к директории с файлами изображений
        :return:
        """
        images_paths = list(paths.list_images(path))
        output_images = list()
        for image_path in images_paths:
            if self.cuda:
                image = self.cuda_detect(image_path)
            else:
                image = self.detect(image_path)
            output_images.append(image)
        return output_images

    def detect(self, image_path: str) -> ndarray:
        """
        Обнаружение объектов на изображении
        :param image_path: Путь к файлу с изображением
        :return: Изображение в виде массива ndarray
        """
        logger.debug(f"{image_path=}")
        image = cv2.imread(image_path)
        image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        cascade = cv2.CascadeClassifier(self.model)
        boxes = cascade.detectMultiScale(image_gray, scaleFactor=1.05, minNeighbors=4)
        for x, y, width, height in boxes:
            cv2.rectangle(image, (x, y), (x + width, y + height), color=(0, 255, 0), thickness=2)
        return image

    def cuda_detect(self, image_path: str) -> ndarray:
        """
        Обнаружение объектов на изображении с применением GPU
        :param image_path: Путь к файлу с изображением
        :return: Изображение в виде массива ndarray
        """
        # Функция написана чисто теоретически.
        # Протестировать не получится, так как видеокарта Intel HD Graphics 4000.
        # Так же, возможно, функция CascadeClassifier устарела для OpenCV 4.9.0
        image = cv2.imread(image_path)
        image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        cascade = cv2.cuda_CascadeClassifier.create(self.model)
        cuFrame = cv2.cuda_GpuMat(image_gray)
        boxes = cascade.detectMultiScale(cuFrame).download()
        for x, y, width, height in boxes:
            cv2.rectangle(image, (x, y), (x + width, y + height), color=(0, 255, 0), thickness=2)
        return image


class FaceDetector(Detector):
    def __init__(self, model: str = haar_face_model, use_cuda: bool = False):
        self.model = model
        self.cuda = use_cuda


if __name__ == "__main__":
    detector = FaceDetector()
    detector.images_handler("/Users/MacAlex/WorkFolder/Python/Projects/RUT/test_data")
