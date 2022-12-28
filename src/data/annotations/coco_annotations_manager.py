from typing import List

from shapely.geometry import Polygon

from src.data.annotations.annotations_manager import AnnotationsManager


class CocoAnnotationsManager(AnnotationsManager):

    def get_image_id(self, image_path):
        return list(filter(lambda image: image['file_name'].endswith(image_path), self.annotations['images']))[0]['id']

    def __get_image_annotation__(self, image_id):
        return list(filter(lambda annotation: annotation['image_id'] == image_id, self.annotations['annotations']))[0]

    def get_annotation(self, image_id):
        """
        Image path is relative to data/
        """

        annotation = self.__get_image_annotation__(image_id)
        return annotation

    def get_bbox(self, image_id):
        """
        Image path is relative to data/
        """

        annotation = self.get_annotation(image_id)
        return annotation["bbox"]

    def get_bbox_polygon(self, image_id):
        """
        https://github.com/cocodataset/cocoapi/issues/34
        """

        bbox = self.get_bbox(image_id)
        x_min, y_min, width, height = bbox
        points = [
            (x_min, y_min),
            (x_min + width, y_min),
            (x_min + width, y_min + height),
            (x_min, y_min + height)
        ]
        return Polygon(points)

    def get_segmentation(self, image_id) -> List:
        """
        https://github.com/cocodataset/cocoapi/issues/102
        """

        annotation = self.get_annotation(image_id)
        return annotation["segmentation"][0]

    def get_segmentation_polygon(self, image_id) -> Polygon:
        """
        Given the image id, this method returns the polygon representing the segmentation of the image annotation
        """
        segmentation = self.get_segmentation(image_id)
        points = []
        for index in range(len(segmentation))[::2]:
            points.append((segmentation[index], segmentation[index+1]))
        return Polygon(points)
