import os

from shapely.geometry import Polygon

from src import utils
from src.data.annotations.coco_annotations_manager import \
    CocoAnnotationsManager

ANNOTATIONS_PATH = os.path.join(utils.DATA_PATH, 'annotations', 'annotations.json')

class TestsCocoAnnotationManager():

    def test_get_annotation(self):
        annotations_manager = CocoAnnotationsManager(ANNOTATIONS_PATH)
        annotation = annotations_manager.get_annotation('1.jpeg')
        
        for field in ["id", "bbox", "area"]:
            assert field in annotation
            
    def test_get_bbox(self):
        annotations_manager = CocoAnnotationsManager(ANNOTATIONS_PATH)
        bbox = annotations_manager.get_bbox('1.jpeg')
        assert isinstance(bbox, list)

    def test_get_bbox_polygon(self):
        annotations_manager = CocoAnnotationsManager(ANNOTATIONS_PATH)
        bbox = annotations_manager.get_bbox_polygon('1.jpeg')
        assert isinstance(bbox, Polygon)
            