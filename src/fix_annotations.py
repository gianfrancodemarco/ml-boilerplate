from src import utils
import os
from src.data.annotations.coco_annotations_manager import CocoAnnotationsManager
from src.features.build_features import flatten_list

ANNOTATIONS_PATH = os.path.join(utils.DATA_PATH, 'annotations', 'test_set_annotations.json')

annotations_manager = CocoAnnotationsManager()
annotations_manager.load_annotations(ANNOTATIONS_PATH)

def fix_annotation(annotation):
    annotation['segmentation'] = [flatten_list(polygon) for polygon in annotation['segmentation']]
    return annotation

annotations_manager.annotations['annotations'] = list(map(fix_annotation, annotations_manager.get_annotations()))
annotations_manager.flush_annotations()