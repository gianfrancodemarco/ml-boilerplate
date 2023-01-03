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
from src import utils
from src.data.annotations.coco_annotations_manager import \
    CocoAnnotationsManager


def pad_or_truncate(some_list, target_len):
    return some_list[:target_len] + [0]*(target_len - len(some_list))

def flatten_list(some_list):
    return list(itertools.chain.from_iterable(some_list))


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


class EarlyStoppingByLossVal(Callback):
    def __init__(self, monitor='val_loss', value=0.0001, verbose=0):
        super(Callback, self).__init__()
        self.monitor = monitor
        self.value = value
        self.verbose = verbose

    def on_epoch_end(self, epoch, logs={}):
        current = logs.get(self.monitor)
        if current is None:
            print("\nEarly stopping requires %s available!" % self.monitor, RuntimeWarning)

        if current < self.value:
            if self.verbose > 0:
                print("\nEpoch %05d: early stopping THR" % epoch)
            self.model.stop_training = True


def build_model(dropout: float = 0):
    input_shape = (512, 512, 3)
    model = Sequential()

    model.add(Input(shape=input_shape))

    # Only for 3 channel images
    model.add(Conv2D(32, 2))
    model.add(LeakyReLU(alpha=0.01))
    model.add(Conv2D(32, 2))
    model.add(LeakyReLU(alpha=0.01))
    model.add(Conv2D(32, 2))
    model.add(LeakyReLU(alpha=0.01))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Conv2D(32, 2))
    model.add(LeakyReLU(alpha=0.01))
    model.add(Conv2D(32, 2))
    model.add(LeakyReLU(alpha=0.01))
    model.add(Conv2D(32, 2))
    model.add(LeakyReLU(alpha=0.01))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Conv2D(32, 2))
    model.add(LeakyReLU(alpha=0.01))
    model.add(Conv2D(32, 2))
    model.add(LeakyReLU(alpha=0.01))
    model.add(Conv2D(32, 2))
    model.add(LeakyReLU(alpha=0.01))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Conv2D(32, 2))
    model.add(LeakyReLU(alpha=0.01))
    model.add(Conv2D(32, 2))
    model.add(LeakyReLU(alpha=0.01))
    model.add(Conv2D(32, 2))
    model.add(LeakyReLU(alpha=0.01))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Flatten())

    if dropout:
        model.add(Dropout(dropout))

    # Only for 3 channel images
    model.add(Dense(128))
    model.add(LeakyReLU(alpha=0.01))

    model.add(Dense(50))
    model.add(LeakyReLU(alpha=0.01))

    model.build()
    model.summary()

    model.compile(loss='mse', optimizer='adam', metrics=[RootMeanSquaredError()])

    return model


def train_model(
        model,
        X,
        y,
        epochs=1000,
        validation_split: float = 0,
        validation_data: Tuple = (),
        early_stopping: bool = False,
        save_every_n_epochs: int = 100,
        save_path = ".",
        model_name = "model"
):

    current_epochs = 0
    model_name += '.h5'

    callbacks = []
    if early_stopping:
        callbacks = [EarlyStoppingByLossVal(monitor='loss', value=1, verbose=1)]

    while current_epochs < epochs:
        current_epochs += save_every_n_epochs

        print(f"Training the model for {save_every_n_epochs} epochs")

        model.fit(
            np.array(X),
            np.array(y),
            epochs=save_every_n_epochs,
            batch_size=16,
            verbose=1,
            validation_split=validation_split,
            callbacks=callbacks,
            validation_data=(np.array(validation_data[0]), np.array(validation_data[1]))
        )
        print("Model trained")

        if save_every_n_epochs:
            print("Saving the model")
            model.save(os.path.join(save_path, model_name))
            print(f"Saved model {model_name}")

    return model


train_X, train_y, validation_X, validation_y = load_data()
model = build_model()
train_model(model, train_X, train_y, validation_data=(validation_X, validation_y), model_name="first_model")
