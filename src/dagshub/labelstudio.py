import hashlib
import json
import os

import cv2

from src import utils

CARD_IMAGES_PATH = os.path.join(utils.DATA_PATH, 'raw', 'templates')
IMAGE_NAME = '1.jpeg'

FILENAME_HASH = hashlib.sha1(os.path.join(CARD_IMAGES_PATH, IMAGE_NAME).encode("utf-8")).hexdigest()
JSON_FILENAME = FILENAME_HASH + '.json'
ANNOTATIONS_PATH = os.path.join(utils.ROOT_PATH, ".labelstudio")

def get_bounding_box_points(
    image_path_from_root,
    source_width,
    source_height
):
    """
    Returns the lablestudio bounding box.
    To retrieve the annotation, this re-computes the SHA1 of the image path, which yelds the annotation filename.
    The path must be the complete path to the image from the root of the project.
    The points of the bounding box are stored as percentages of the image. To convert them to absolute values, the width and height of the original
    image are used. 
    If they are passed as parameters, these are used. Otherwise, the image will be loaded using the path to retrieve its width and height
    """

    FILENAME_HASH = hashlib.sha1((image_path_from_root).encode("utf-8")).hexdigest()
    JSON_FILENAME = FILENAME_HASH + '.json'

    ANNOTATION = json.loads(open(os.path.join(ANNOTATIONS_PATH, JSON_FILENAME)).read())

    if not (source_width and source_height):
        image = cv2.imread(image_path_from_root)
        source_width, source_height, _ = image.shape

    def rel_point_to_abs_point(x, y):
        return (source_width/100*x, source_height/100*y)

    points = ANNOTATION['annotations'][0]['result'][0]['value']['points']
    points = [rel_point_to_abs_point(x,y) for (x,y) in (couple for couple in points)]

    return points