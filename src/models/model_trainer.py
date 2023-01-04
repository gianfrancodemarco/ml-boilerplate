import logging

from keras.callbacks import Callback


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
        save_every_n_epochs: int = 3,
):
        current_epochs = 0
        callbacks = []
        if early_stopping:
            callbacks = [EarlyStoppingByLossVal(monitor='loss', value=1, verbose=1)]

        while current_epochs < epochs:
            current_epochs += save_every_n_epochs

            logging.info(f"Training the model for {save_every_n_epochs} epochs")
            model.fit(
                x = dataset,
                validation_data = validation_dataset,
                epochs=save_every_n_epochs,
                batch_size=16,
                verbose=1,
                validation_split=validation_split,
                callbacks=callbacks,
            )
            logging.info(f"Model fitted for {save_every_n_epochs} epochs")

            if save_every_n_epochs:
                yield model

        return model