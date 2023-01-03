import json
from typing import List

from shapely.geometry import Polygon
from src.data.annotations.annotations_manager import AnnotationsManager

class CocoAnnotationsManager(AnnotationsManager):

    def get_images(self):
        return self.annotations['images']

    def get_annotations(self):
        return self.annotations['annotations']

    def get_image_id(self, image_path):
        return list(filter(lambda image: image['file_name'].endswith(image_path), self.annotations['images']))[0]['id']

    def __get_image_annotations__(self, image_id):
        return list(filter(lambda annotation: annotation['image_id'] == image_id, self.annotations['annotations']))

    def get_image_annotations(self, image_id):
        """
        Image path is relative to data/
        """
        return self.__get_image_annotations__(image_id)
        
    def get_bboxes(self, image_id):
        """
        Image path is relative to data/
        """

        annotations = self.get_image_annotations(image_id)
        return list(map(lambda annotation: annotation["bbox"], annotations))

    def get_bboxes_polygons(self, image_id):
        """
        https://github.com/cocodataset/cocoapi/issues/34
        """

        bboxes = self.get_bboxes(image_id)
        polygons = []

        for bbox in bboxes:
            x_min, y_min, width, height = bbox
            
            # TODO: Maybe can be replaced by doing Polygon(segmentation).bounds
            points = [
                (x_min, y_min),
                (x_min + width, y_min),
                (x_min + width, y_min + height),
                (x_min, y_min + height)
            ]
            polygons.append(Polygon(points))
            
        return polygons

    def get_segmentations(self, image_id) -> List:
        """
        https://github.com/cocodataset/cocoapi/issues/102
        """

        annotations = self.get_image_annotations(image_id)
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

    def create_empty_annotations(
        self, 
        annotations_path,
        images: List[dict] = [],
        categories: List[dict] = [],
        annotations: List[dict] = [],
        info: dict = {}
        ):
        "Creates a new COCO annotations file and loads it into memory"

        self.annotations_path = annotations_path
        with open(self.annotations_path, mode='w', encoding='utf-8') as file:
            self.annotations = {
                "images": images,
                "categories": categories,
                "annotations": annotations,
                "info": info
            }
            file.write(json.dumps(self.annotations, indent=4))

    def add_image(
        self, 
        width: int,
        height: int,
        filename: str
    ):
        """
        Add image to the annotations, return the generated image id
        """

        image_id = len(self.annotations['images'])

        self.annotations['images'].append(
            {
                "width": width,
                "height": height,
                "id": image_id,
                "file_name": filename
            }
        )

        return image_id


    def add_annotation(
        self, 
        image_id: int,
        category_id : int,
        segmentation: List[List[float]],
        bbox: List[float],
        area: float,
        ignore: int = 0,
        iscrowd: int = 0      
    ):

        annotation_id = len(self.annotations['annotations'])
        self.annotations['annotations'].append(
            {
                "id": annotation_id,
                "image_id": image_id,
                "category_id": category_id,
                "segmentation": segmentation,
                "bbox": bbox,
                "ignore": ignore,
                "iscrowd": iscrowd,
                "area": area
            }
        )

        return annotation_id

    def flush_annotations(self):
        "Save annotations to memory at self.annotations_path"

        with open(self.annotations_path, mode='w', encoding='utf-8') as file:
            file.write(json.dumps(self.annotations, indent=4))