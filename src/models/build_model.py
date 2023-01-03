from keras.layers import (Conv2D, Dense, Dropout, Flatten, Input, LeakyReLU,
                          MaxPooling2D)
from keras.metrics import RootMeanSquaredError
from keras.models import Sequential


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
