import itertools
import os
from typing import Tuple

import cv2
import numpy as np
import tensorflow as tf
from keras.callbacks import Callback
from src import utils
from src.data.annotations.coco_annotations_manager import \
    CocoAnnotationsManager
from src.features.dataset import ImagesDatasetGenerator
from src.models.build_model import build_model

train_annotations_path = os.path.join(utils.DATA_PATH, 'annotations', 'train_set_annotations.json')
train_annotations_manager = CocoAnnotationsManager()
train_annotations_manager.load_annotations(train_annotations_path)
train_images_base_path = os.path.join(utils.DATA_PATH, 'processed', 'train')
train_images_paths =  [os.path.join(train_images_base_path, image['file_name']) for image in train_annotations_manager.get_images()]
train_dataset_generator = ImagesDatasetGenerator(
    images_paths=train_images_paths[:100],
    annotations=train_annotations_manager.get_flattened_segmentations(),
    pad_annotations=50
)

train_dataset = tf.data.Dataset.from_generator(
    train_dataset_generator.get_image,
    output_signature=(tf.TensorSpec(shape=(512, 512, 3)), tf.TensorSpec(shape=(50, )))
)

validation_annotations_path = os.path.join(utils.DATA_PATH, 'annotations', 'validation_set_annotations.json')
validation_annotations_manager = CocoAnnotationsManager()
validation_annotations_manager.load_annotations(validation_annotations_path)
validation_images_base_path = os.path.join(utils.DATA_PATH, 'processed', 'validation')
validation_images_paths =  [os.path.join(validation_images_base_path, image['file_name']) for image in validation_annotations_manager.get_images()]
validation_dataset_generator = ImagesDatasetGenerator(
    images_paths=validation_images_paths[:100],
    annotations=validation_annotations_manager.get_flattened_segmentations(),
    pad_annotations=50
)

validation_dataset = tf.data.Dataset.from_generator(
    validation_dataset_generator.get_image,
    output_signature=(tf.TensorSpec(shape=(512, 512, 3)), tf.TensorSpec(shape=(50, )))
)

def configure_for_performance(ds):
  ds = ds.cache()
  ds = ds.shuffle(buffer_size=1000)
  ds = ds.batch(16)
  ds = ds.prefetch(buffer_size=tf.data.AUTOTUNE)
  return ds

train_dataset = configure_for_performance(train_dataset)
validation_dataset = configure_for_performance(validation_dataset)

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

def train_model(
        model,
        dataset,
        validation_dataset,
        epochs=1000,
        validation_split: float = 0,
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
            x = dataset,
            validation_data = validation_dataset,
            epochs=save_every_n_epochs,
            batch_size=16,
            verbose=1,
            validation_split=validation_split,
            callbacks=callbacks,
        )
        print("Model trained")

        if save_every_n_epochs:
            print("Saving the model")
            model.save(os.path.join(save_path, model_name))
            print(f"Saved model {model_name}")

    return model

model = build_model()
train_model(model, dataset = train_dataset, validation_dataset=validation_dataset, model_name="first_model")
