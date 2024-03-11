import logging
import os

from numpy import ndarray
import settings

import cv2

from utils.image_tools import convert_image_to_bytes

logger = logging.getLogger("logger")

cv2_base_dir = os.path.dirname(os.path.abspath(cv2.__file__))
haar_face_model = os.path.join(cv2_base_dir, 'data/haarcascade_frontalface_alt.xml')


class Detector:
    """Класс обнаружения объектов на изображениях"""

    def __init__(self, model: str, use_cuda: bool = False):
        self.model = model
        self.cuda = use_cuda
        self.scaleFactor = 1.05
        self.minNeighbors = 4

    def processed_image_generator(self, images_paths: list[str]) -> list[ndarray]:
        """
        Генератор обработанных изображений из указанной директории
        :param images_paths: Список путей файлов с изображениями
        :return:
        """
        for image_path in images_paths:
            if self.cuda:
                image = self.cuda_detect(image_path)
            else:
                image = self.detect(image_path)
            yield image

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
        boxes = cascade.detectMultiScale(image_gray, self.scaleFactor, self.minNeighbors)
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
        super().__init__(model, use_cuda)


def detect_faces_and_save(images: list[str], path_to: str = None, prefix: str = '') -> list:
    """
    Обнаруживает лица на изображениях и сохраняет в новый файл или перезаписывает
    :param images: Список путей файлов с изображениями
    :param path_to: Путь для сохранения новых файлов
    :param prefix: Префикс для новых файлов с изображениями
    :return: Список имен новых файлов с изображениями
    """
    logger.debug(f'{images=}')
    detector = FaceDetector()
    new_filenames = []
    i = 0
    for image in detector.processed_image_generator(images):
        image_bytes = convert_image_to_bytes(image)
        new_filename = f'{prefix}{os.path.basename(images[i])}'
        new_filenames.append(new_filename)
        if path_to:
            new_file_path = os.path.join(path_to, new_filename)
        else:
            new_file_path = os.path.join(os.path.dirname(images[i]), new_filename)
        with open(new_file_path, "wb") as new_image:
            new_image.write(image_bytes)
        i += 1
    return new_filenames
