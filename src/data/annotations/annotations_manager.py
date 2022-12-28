import json
from abc import abstractmethod

from shapely.geometry import Polygon


class AnnotationsManager:
    def __init__(
        self,
        annotations_path: str
    ) -> None:
        self.annotations_path = annotations_path

        with open(self.annotations_path, mode='r', encoding='utf-8') as file:
            self.annotations = json.loads(file.read())

    def get_annotations(self):
        return self.annotations

    @abstractmethod
    def get_segmentation_polygon(self, image_id) -> Polygon:
        """
        Given the image id, this method should return the polygon representing the segmentation of the image annotation
        """
