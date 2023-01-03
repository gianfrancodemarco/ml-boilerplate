import json
import logging
import os
from abc import abstractmethod
from typing import List, Tuple

import cv2
import numpy as np
from shapely.geometry import Polygon
from src import utils
from src.data.annotations.annotations_manager import AnnotationsManager
from src.data.misc import (
    get_random_translated_polygon_in_boundary_and_not_overlapping,
    sort_2d_points)


class ImageTemplate:
    """An image template, that can be used to generate other images.
    An instance of ImageTemplate is created by passing a configuration object

    Attributes:
        image_path              The image path relative to the data folder
        image_id                Image id to as associated in the annotations
        type                    FIXED or DYNAMIC
        ignore                  If true, the template will won't be returned by getters methods
        segmentation            Polygon of the image annotation
        annotation_manager      Used to retrieve the image annotation
    """

    image_path: str
    image_id: str
    type: str
    ignore: bool
    segmentation_polygons: List[Polygon]
    annotation_manager: AnnotationsManager
    

    def __init__(
        self,
        config: dict,
        annotations_manager: AnnotationsManager
    ) -> None:
        self.image_id = config['image_id']
        self.image_path = config['image_path']
        self.image = cv2.cvtColor(
            cv2.imread(os.path.join(utils.ROOT_PATH, self.image_path)),
            cv2.COLOR_BGR2RGB
        )
        self.ignore = config.get('ignore', False)
        self.annotation_manager = annotations_manager
        self.segmentation_polygons = self.annotation_manager.get_segmentation_polygons(
            self.image_id)

    @abstractmethod
    def generate_image(self, patch: np.ndarray) -> Tuple[np.ndarray, Polygon]:
        """
        Generate an image from this template.
        The image is generated by applying the patch to the template image. The implementation depends on the subclass

        Returns a pair: (the new image, the new image segmentation polygon)
        """

    def __transform_patch_into_polygon__(
        self,
        patch: np.ndarray,
        polygon: Polygon,
        destination_image: np.ndarray
    ) -> np.ndarray:
        """
        Applies the geometric transformations required to transform the patch in the polygon's shape.
        The destination image is required so that the transformed patch is placed in an image of correct dimensions
        """

        # Adjust the patch to match the segmentation polygon
        src_points = [
            [0, 0],
            [0, patch.shape[0]-1],
            [patch.shape[1]-1, 0],
            [patch.shape[1]-1, patch.shape[0]-1]
        ]
        src_points = np.float32(self.__reorder_segmentation_points__(src_points))

        # Remove the last point, which is == to the first to close the polygon
        dst_points = list(polygon.exterior.coords)[:-1]
        dst_points = np.float32(self.__reorder_segmentation_points__(dst_points))

        transformation_matrix = cv2.getPerspectiveTransform(
            src_points, dst_points
        )
        trans_img = cv2.warpPerspective(
            patch,
            transformation_matrix,
            (destination_image.shape[1], destination_image.shape[0])
        )

        return trans_img

    def __reorder_segmentation_points__(self, points: List):
        """
        Returns points ordered in clockwise fashion
        """
        return sort_2d_points(points)

    def __stich_path_to_image__(
        self,
        patch: np.ndarray,
        dst_image: np.ndarray,
        polygon: np.ndarray
    ) -> np.ndarray:

        dst_image = dst_image.copy()
        coords = [np.array(polygon.exterior.coords).round().astype(np.int32)]
        cv2.fillPoly(dst_image, coords, color=(0, 0, 0))
        dst_image = cv2.add(dst_image, patch)

        return dst_image


class FixedImageTemplate(ImageTemplate):
    def __init__(self, config: dict, annotations_manager: AnnotationsManager) -> None:
        super().__init__(config, annotations_manager)
        self.type = "FIXED"

    def generate_image(self, patches: List[np.ndarray]) -> Tuple[np.ndarray, List[Polygon]]:
        """
        Generate an image from this template.
        The image is generated by applying the patch to the template image.
        The patch is overlapped to the original segmentation polygon

        Returns a pair: (the new image, the template segmentation polygon)
        """

        if len(patches) != len(self.segmentation_polygons):
            raise ValueError(
                f"{len(self.segmentation_polygons)} patches are needed, but {len(patches)} patches were provided")

        patched_image = self.image.copy()

        for (patch, polygon) in zip(patches, self.segmentation_polygons):
            trans_patch = self.__transform_patch_into_polygon__(patch, polygon, patched_image)
            patched_image = self.__stich_path_to_image__(trans_patch, patched_image, polygon)

        return (patched_image, self.segmentation_polygons)


class DynamicImageTemplate(ImageTemplate):
    """
    Attributes:
        background_path         The path to the background image for this template
        max_patches             The max number of patches that is possible to apply to this template. This is set in the configuration
                                based on the patch size and the background size
    """

    def __init__(self, config: dict, annotations_manager: AnnotationsManager) -> None:
        super().__init__(config, annotations_manager)
        self.type = "DYNAMIC"
        self.background_path = config['background_path']
        self.background_image = cv2.cvtColor(
            cv2.imread(os.path.join(utils.ROOT_PATH, self.background_path)),
            cv2.COLOR_BGR2RGB
        )
        self.max_patches = config['max_patches']

        if len(self.segmentation_polygons) != 1:
            raise ValueError("Exactly 1 segementation_polygon is required for a DYNAMIC template")

    def generate_image(self, patches: List[np.ndarray]) -> Tuple[np.ndarray, List[Polygon]]:
        """
        Generate an image from this template.
        The image is generated by applying the patches to the template's background in random positions, without overlapping.
        The number of patches must be <= to the template's max_patches attribute

        Returns a pair: (the new image, the patches segmentation polygons)
        """

        if len(patches) > self.max_patches:
            raise ValueError(
                f"A maximum of {len(self.max_patches)} is supported, but {len(patches)} patches were provided")

        patched_image = self.background_image.copy()
        generated_polygons = []
        polygon = self.segmentation_polygons[0]

        for patch in patches:
            translated_polygon, succeeded = get_random_translated_polygon_in_boundary_and_not_overlapping(
                polygon, patched_image.shape[1], patched_image.shape[0], generated_polygons)

            if not succeeded:
                logging.warning(
                    "It was not possible to generate a non-overlapping translation. Skipping this patch")
                continue

            generated_polygons.append(translated_polygon)
            trans_patch = self.__transform_patch_into_polygon__(
                patch, translated_polygon, patched_image)
            patched_image = self.__stich_path_to_image__(
                trans_patch, patched_image, translated_polygon)

        return (patched_image, generated_polygons)


class ImagesTemplatesManager:
    templates_config_path: str
    templates_config: dict
    annotation_manager: AnnotationsManager
    templates: List[ImageTemplate]

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
                template_class = FixedImageTemplate
            elif template_config["type"] == "DYNAMIC":
                template_class = DynamicImageTemplate

            try:
                template = template_class(template_config, annotation_manager)
                self.templates.append(template)
            except Exception as e:
                logging.warn("Could not load template with config:")
                logging.warn(template_config) 
                logging.error(e)

    def get_template_by_image_id(
        self,
        image_id: int
    ) -> ImageTemplate:
        return list(filter(lambda template: template.image_id == image_id, self.templates))[0]

    def get_templates(self) -> List[ImageTemplate]:
        return self.templates

    def get_fixed_templates(self) -> List[ImageTemplate]:
        return list(filter(lambda template: template.type == "FIXED" and not template.ignore, self.templates))

    def get_dynamic_templates(self) -> List[ImageTemplate]:
        return list(filter(lambda template: template.type == "DYNAMIC" and not template.ignore, self.templates))
