from typing import List

from shapely.geometry import Polygon

from src.data.annotations.annotations_manager import AnnotationsManager


class CocoAnnotationsManager(AnnotationsManager):

    def get_image_id(self, image_path):
        return list(filter(lambda image: image['file_name'].endswith(image_path), self.annotations['images']))[0]['id']

    def __get_image_annotations__(self, image_id):
        return list(filter(lambda annotation: annotation['image_id'] == image_id, self.annotations['annotations']))

    def get_annotations(self, image_id):
        """
        Image path is relative to data/
        """

        return self.__get_image_annotations__(image_id)
        
    def get_bboxes(self, image_id):
        """
        Image path is relative to data/
        """

        annotations = self.get_annotations(image_id)
        return list(map(lambda annotation: annotation["bbox"], annotations))

    def get_bbox_polygon(self, image_id):
        """
        https://github.com/cocodataset/cocoapi/issues/34
        """

        bbox = self.get_bbox(image_id)
        x_min, y_min, width, height = bbox
        
        # TODO: Maybe can be replaced by doing Polygon(segmentation).bounds
        points = [
            (x_min, y_min),
            (x_min + width, y_min),
            (x_min + width, y_min + height),
            (x_min, y_min + height)
        ]
        return Polygon(points)

    def get_segmentations(self, image_id) -> List:
        """
        https://github.com/cocodataset/cocoapi/issues/102
        """

        annotations = self.get_annotations(image_id)
        return list(map(lambda annotation: annotation["segmentation"][0], annotations))

    def get_segmentation_polygons(self, image_id) -> List[Polygon]:
        """
        Given the image id, this method returns the polygon representing the segmentations of the image annotation
        """
        segmentations = self.get_segmentations(image_id)
        polygons = []
        
        for segmentation in segmentations:
            points = []
            for index in range(len(segmentation))[::2]:
                points.append((segmentation[index], segmentation[index+1]))
            polygons.append(Polygon(points))
        
        return polygons
