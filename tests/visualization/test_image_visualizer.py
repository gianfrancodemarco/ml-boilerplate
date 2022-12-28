import os

import cv2
from shapely.geometry import Polygon

from src import utils
from src.data.annotations.coco_annotations_manager import \
    CocoAnnotationsManager
from src.visualization.image_visualizer import show_image

ANNOTATIONS_PATH = os.path.join(utils.TESTS_PATH, 'assets', 'annotations.json')
CARD_IMAGES_PATH = os.path.join(utils.TESTS_PATH, 'assets')
IMAGE_NAME = '1.jpeg'

IMAGE_PATH = os.path.join('..', CARD_IMAGES_PATH, IMAGE_NAME)
IMAGE_PATH_RELATIVE_TO_DATA = os.path.join('tests', 'assets', IMAGE_NAME)
IMAGE = cv2.imread(IMAGE_PATH)

class TestsImageVisualizer():

    def test_show_image(self):
        assert show_image(IMAGE)
        annotations_manager = CocoAnnotationsManager(ANNOTATIONS_PATH)
        bbox = annotations_manager.get_bbox_polygon(image_path=IMAGE_PATH_RELATIVE_TO_DATA)
        assert show_image(IMAGE, bbox)