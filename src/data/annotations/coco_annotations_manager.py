from shapely.geometry import Polygon

from src.data.annotations.annotations_manager import AnnotationsManager


class CocoAnnotationsManager(AnnotationsManager):

    def __get_image_id__(self, image_path):
        return list(filter(lambda image: image['file_name'].endswith(image_path), self.annotations['images']))[0]['id']
    
    def __get_image_annotation__(self, image_id):
        return list(filter(lambda annotation: annotation['image_id'] == image_id, self.annotations['annotations']))[0]
    
    def get_annotation(self, image_path):
        """
        Image path is relative to data/
        """

        image_id = self.__get_image_id__(image_path)
        annotation =  self.__get_image_annotation__(image_id)
        return annotation

    def get_bbox(self, image_path):
        """
        Image path is relative to data/
        """

        annotation = self.get_annotation(image_path=image_path)
        return annotation["bbox"]
        
    def get_bbox_polygon(self, image_path):
        bbox = self.get_bbox(image_path)
        points = list(zip(bbox, bbox[1:]))
        return Polygon(points)
