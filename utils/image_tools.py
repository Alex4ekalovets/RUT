import logging
from typing import Tuple

import cv2
import numpy as np
from numpy import ndarray

logger = logging.getLogger("logger")


class ImageHandlers:
    """Класс обработчиков изображений"""

    @classmethod
    def resize(
            cls,
            image: ndarray,
            height: int,
            width: int,
            save_ratio: bool = False,
            side: str = None,
    ) -> ndarray:
        """
        Изменение размера изображения
        :param image: Изображение в виде массива ndarray
        :param height: Высота конечного изображения
        :param width: Ширина конечного изображения
        :param save_ratio: Сохранение пропорций изображения
        :param side: Сторона, относительно которой необходимо сохранять пропорции ("width"/"height")
        :return: Изображение в виде массива ndarray
        """
        default_height, default_width, _ = image.shape
        if save_ratio:
            if side == "width":
                height = int((width * default_height) / default_width)
            elif side == "height":
                width = int((height * default_width) / default_height)
        image = cv2.resize(src=image, dsize=(width, height))
        return image

    @classmethod
    def crop(
            cls, image: ndarray, top: int, bottom: int, left: int, right: int
    ) -> ndarray:
        """
        Обрезка изображения
        :param image: Изображение в виде массива ndarray
        :param top: Количество обрезаемых пикселей сверху
        :param bottom: Количество обрезаемых пикселей снизу
        :param left: Количество обрезаемых пикселей слева
        :param right: Количество обрезаемых пикселей справа
        :return: Изображение в виде массива ndarray
        """
        height, width, _ = image.shape
        image = image[top: (height - bottom), left: (width - right)]
        return image

    @classmethod
    def rotate(cls, image: ndarray, angle: int) -> ndarray:
        """
        Поворот изображения
        :param image: Изображение в виде массива ndarray
        :param angle: Угол поворота
        :return: Изображение в виде массива ndarray
        """
        height, width, _ = image.shape
        angles = {
            90: cv2.ROTATE_90_COUNTERCLOCKWISE,
            180: cv2.ROTATE_180,
            -90: cv2.ROTATE_90_CLOCKWISE,
            270: cv2.ROTATE_90_CLOCKWISE,
            -270: cv2.ROTATE_90_COUNTERCLOCKWISE,
        }
        if angle in angles.keys():
            image = cv2.rotate(image, angles[angle])
        else:
            image_center = (width / 2, height / 2)
            rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
            image = cv2.warpAffine(
                image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR
            )
        return image

    @classmethod
    def blur(cls, image: ndarray, blur: int) -> ndarray:
        """
        Размытие
        :param image: Изображение в виде массива ndarray
        :param blur: Величина размытия
        :return: Изображение в виде массива ndarray
        """
        if blur >= 0:
            image = cv2.medianBlur(image, 1 + blur * 2)
        return image

    @classmethod
    def rgb(cls, image: ndarray, red: int, green: int, blue: int) -> ndarray:
        """
        Изменение уровней цветов
        :param image: Изображение в виде массива ndarray
        :param red: Уровень красного цвета -255...255
        :param green: Уровень зеленого цвета -255...255
        :param blue: Уровень синего цвета -255...255
        :return: Изображение в виде массива ndarray
        """
        bgr = list(cv2.split(image))
        bgr_add = [blue, green, red]

        for i in range(3):
            if bgr_add[i] > 0:
                bgr[i] = np.where(bgr[i] <= 255 - bgr_add[i], bgr[i] + bgr_add[i], 255)
            else:
                bgr[i] = np.where(
                    bgr[i] > abs(bgr_add[i]), bgr[i] + bgr_add[i], 0
                ).astype(bgr[i].dtype)

        image = cv2.merge(bgr)
        return image


def image_handler(
        image_path: str, handlers: ImageHandlers = ImageHandlers, **kwargs
) -> ndarray:
    """
    Применение обработчиков к изображению
    :param image_path: Путь к файлу изображения
    :param handlers: Класс обработчиков изображения
    :param kwargs: Словарь: ключ - имя обработчика, значение - аргументы функции-обработчика
    :return: Изображение в виде массива ndarray
    """
    image = cv2.imread(image_path)
    for handler, params in kwargs.items():
        handler_method = getattr(handlers, handler)
        if handler_method:
            image = handler_method(image=image, **params)
    return image


def get_image_size(image_path: str) -> Tuple[int, int]:
    """
    Получение размеров изображения
    :param image_path: Путь к файлу с изображением
    :return: Кортеж(высота, ширина)
    """
    image = cv2.imread(image_path)
    height, width, _ = image.shape
    return height, width


def convert_image_to_bytes(image: str | ndarray) -> bytes:
    """
    Преобразование изображения в байты
    :param image: Путь к файлу с изображением или массив ndarray
    :return: Массив байтов
    """
    if isinstance(image, str):
        image = cv2.imread(image)
    elif not isinstance(image, ndarray):
        raise TypeError(
            "Передайте путь к изображению в виде строки или изображение в виде numpy массива"
        )
    ret, image = cv2.imencode(".jpg", image)
    image = image.tobytes()
    return image


if __name__ == "__main__":
    pass
