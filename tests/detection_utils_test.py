import time

from imutils import paths

from utils.detection import detect_faces_and_save


def test_detect_faces_and_save():
    start = time.time()
    images = list(paths.list_images(r".\tests\data\faces_dataset"))
    detect_faces_and_save(images=images)
    execution_time = time.time() - start
    fps = len(images) / execution_time
    assert fps > 24
