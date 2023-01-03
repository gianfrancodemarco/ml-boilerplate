import itertools
import os
from typing import Tuple

import cv2
import numpy as np
import tensorflow.keras as keras
from keras.callbacks import Callback
from keras.layers import (AveragePooling2D, BatchNormalization, Conv2D, Dense,
                          Dropout, Flatten, Input, LeakyReLU, MaxPooling2D)
from keras.metrics import MeanSquaredError, RootMeanSquaredError
from keras.models import Sequential, load_model
from shapely.geometry import Polygon
from src import utils
from src.data.annotations.coco_annotations_manager import \
    CocoAnnotationsManager
from src.visualization.image_visualizer import show_image


def pad_or_truncate(some_list, target_len):
    return some_list[:target_len] + [0]*(target_len - len(some_list))

def flatten_list(some_list):
    return list(itertools.chain.from_iterable(some_list))

model = load_model('first_model.h5')

def load_data():
    TRAIN_ANNOTATIONS_PATH = os.path.join(utils.DATA_PATH, 'annotations', 'train_set_annotations.json')
    annotations_manager = CocoAnnotationsManager()
    annotations_manager.load_annotations(TRAIN_ANNOTATIONS_PATH)
    train_X = [cv2.resize(cv2.imread(os.path.join(utils.DATA_PATH, 'processed', 'train', image['file_name'])), (512,512)) for image in annotations_manager.get_images()[:2]]
    train_y = [
        pad_or_truncate(flatten_list(segmentation), 50) for segmentation in
            [[flatten_list(segmentation) for segmentation in 
                annotation['segmentation']] for annotation in 
                    annotations_manager.get_annotations()[:2]
            ]
        ]

    VALIDATION_ANNOTATIONS_PATH = os.path.join(utils.DATA_PATH, 'annotations', 'validation_set_annotations.json')
    annotations_manager = CocoAnnotationsManager()
    annotations_manager.load_annotations(VALIDATION_ANNOTATIONS_PATH)
    validation_X = [cv2.resize(cv2.imread(os.path.join(utils.DATA_PATH, 'processed', 'train', image['file_name'])), (512,512)) for image in annotations_manager.get_images()[:2]]
    validation_y = [
        pad_or_truncate(flatten_list(segmentation), 50) for segmentation in
            [[flatten_list(segmentation) for segmentation in 
                annotation['segmentation']] for annotation in 
                    annotations_manager.get_annotations()[:2]
            ]
        ]

    return train_X, train_y, validation_X, validation_y

train_X, train_y, validation_X, validation_y = load_data()
polygons = model.predict(np.array([(np.array(train_X[0]))]))
polygons = np.array_split([el/(1500/512) if el > 0 else 0 for el in polygons[0]], 5)
polygons = [Polygon(np.array_split(polygon, 4)) for polygon in polygons]
show_image(train_X[0], polygons)