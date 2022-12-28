import json
from typing import List

from shapely.geometry import Polygon

from src.data.annotations.annotations_manager import AnnotationsManager


class ImageTemplate:

    image_path: str
    image_id: str
    type: str
    segmentation: Polygon

    def __init__(
        self,
        config: dict
    ) -> None:
        self.image_path = config['image']
        self.image_id = config['image_id']

    def load_annotation(
        self,
        annotations_manager: AnnotationsManager
    ):
        """
        Loads the annotation for the template image using the annotation manager
        """
        self.segmentation = annotations_manager.get_segmentation_polygon(self.image_id)

class FixedImageTemplate(ImageTemplate):
    def __init__(self, config: dict) -> None:
        super().__init__(config)
        self.type = "FIXED"


class DynamicImageTemplate(ImageTemplate):
    def __init__(self, config: dict) -> None:
        super().__init__(config)
        self.type = "DYNAMIC"


class ImagesTemplatesManager:
    templates_config_path: str
    templates_config: dict
    annotation_manager: AnnotationsManager
    templates: List

    def __init__(
        self,
        templates_config_path: str,
        annotation_manager: AnnotationsManager
    ) -> None:
        self.templates_config_path = templates_config_path
        self.annotation_manager = annotation_manager

        with open(self.templates_config_path, mode='r', encoding='utf-8') as file:
            self.templates_config = json.loads(file.read())

        self.templates = []
        for template_config in self.templates_config:
            # TODO: This could replaced by a factory
            template = None
            if template_config["type"] == "FIXED":
                template = FixedImageTemplate(template_config)
            elif template_config["type"] == "DYNAMIC":
                template = DynamicImageTemplate(template_config)

            template.load_annotation(self.annotation_manager)
            self.templates.append(template)

    def get_template_by_image_id(
        self,
        image_id: int
    ) -> ImageTemplate:
        return list(filter(lambda template: template.image_id == image_id), self.templates)[0]
