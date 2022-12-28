import os

from shapely.geometry import Polygon

from src import utils
from src.data.annotations.coco_annotations_manager import \
    CocoAnnotationsManager

ANNOTATIONS_PATH = os.path.join(utils.TESTS_PATH, 'assets', 'annotations.json')
class TestsCocoAnnotationManager():

    def test_get_annotation(self):
        annotations_manager = CocoAnnotationsManager(ANNOTATIONS_PATH)
        image_id = annotations_manager.get_image_id('1.jpeg')
        annotation = annotations_manager.get_annotation(image_id=image_id)
        
        for field in ["id", "bbox", "area"]:
            assert field in annotation
            
    def test_get_bbox(self):
        annotations_manager = CocoAnnotationsManager(ANNOTATIONS_PATH)
        image_id = annotations_manager.get_image_id('1.jpeg')
        bbox = annotations_manager.get_bbox(image_id=image_id)
        assert isinstance(bbox, list)

    def test_get_bbox_polygon(self):
        annotations_manager = CocoAnnotationsManager(ANNOTATIONS_PATH)
        image_id = annotations_manager.get_image_id('1.jpeg')
        polygon = annotations_manager.get_bbox_polygon(image_id=image_id)
        assert isinstance(polygon, Polygon)
            