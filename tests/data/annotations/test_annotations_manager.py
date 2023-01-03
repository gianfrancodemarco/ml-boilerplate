import os

from src import utils
from src.data.annotations.annotations_manager import AnnotationsManager

ANNOTATIONS_PATH = os.path.join(utils.DATA_PATH, 'annotations', 'annotations.json')

class TestsAnnotationsManager():

    def test_annotations_manager(self):
        annotations_manager = AnnotationsManager(ANNOTATIONS_PATH)
        annotations = annotations_manager.get_image_annotations()
        assert annotations
        