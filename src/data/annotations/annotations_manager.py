import json
from abc import abstractmethod

from shapely.geometry import Polygon


class AnnotationsManager:

    annotations_path: str 

    def load_annotations(self, annotations_path):
        self.annotations_path = annotations_path
        with open(self.annotations_path, mode='r', encoding='utf-8') as file:
            self.annotations = json.loads(file.read())

    def get_image_annotations(self):
        return self.annotations

    def create_empty_annotations(self, annotations_path):
        "Creates a new annotations file and loads it into memory"

        self.annotations_path = annotations_path
        with open(self.annotations_path, mode='w', encoding='utf-8') as file:
            self.annotations = {}
            file.write(json.dumps(self.annotations, indent=4))

    @abstractmethod
    def add_annotation(annotation):
        pass

    @abstractmethod
    def get_segmentation_image_polygons(self, image_id) -> Polygon:
        """
        Given the image id, this method should return the polygons representing the segmentations of the image annotation
        """

    