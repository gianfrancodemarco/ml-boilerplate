import os

from shapely.geometry import Polygon
from src import utils
from src.data.annotations.coco_annotations_manager import \
    CocoAnnotationsManager

ANNOTATIONS_PATH = os.path.join(utils.TESTS_PATH, 'assets', 'annotations.json')
class TestsCocoAnnotationManager():

    def test_get_image_annotations(self):
        annotations_manager = CocoAnnotationsManager(ANNOTATIONS_PATH)
        image_id = annotations_manager.get_image_id('1.jpeg')
        annotations = annotations_manager.get_image_annotations(image_id=image_id)
        
        for annotation in annotations:
            for field in ["id", "bbox", "area"]:
                assert field in annotation
            
    def test_get_bboxes(self):
        annotations_manager = CocoAnnotationsManager(ANNOTATIONS_PATH)
        image_id = annotations_manager.get_image_id('1.jpeg')
        bboxes = annotations_manager.get_bboxes(image_id=image_id)
        assert isinstance(bboxes, list)
        assert isinstance(bboxes[0], list)

    def test_get_bboxes_polygon(self):
        annotations_manager = CocoAnnotationsManager(ANNOTATIONS_PATH)
        image_id = annotations_manager.get_image_id('1.jpeg')
        polygons = annotations_manager.get_bboxes_polygons(image_id=image_id)
        assert isinstance(polygons, list)
        assert isinstance(polygons[0], Polygon)
            