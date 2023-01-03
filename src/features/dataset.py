import logging

import cv2
import numpy as np
from src.features.build_features import pad_or_truncate


class ImagesDatasetGenerator():

    def __init__(
        self, 
        images_paths,
        annotations,
        pad_annotations: int = None
    ):
        self.images_paths = images_paths
        if pad_annotations:
            self.annotations = np.array([pad_or_truncate(annotation, pad_annotations) for annotation in annotations])
        else:
            self.annotations = np.array(annotations)
    
    def get_image(self):
        for (image_path, annotation) in zip(self.images_paths, self.annotations):
            try:
                image = cv2.imread(image_path)
                image = cv2.resize(image, (512, 512))
                yield image, annotation
            except:
                logging.error(image_path)
                logging.error(annotation)
