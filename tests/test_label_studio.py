import logging
import os

from src import utils
from src.dagshub.labelstudio import get_bounding_box_points

CARD_IMAGES_PATH = os.path.join('data', 'raw', 'templates')
IMAGE_NAME = '1.jpeg'

class TestsLabelStudio():

    def test_label_studio(self):
        assert get_bounding_box_points(os.path.join(CARD_IMAGES_PATH, IMAGE_NAME), 1500, 1500)