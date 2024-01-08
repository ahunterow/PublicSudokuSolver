import tensorflow
import settings

class Network:
    """Represents the model of the neural network for solving sudokus, THIS CLASS WAS INSPIRED BY SHIVAVARMA'S MODEL."""
    def __init__(self, input_shape):

        model = tensorflow.keras.Sequential()
        model.add(tensorflow.keras.layers.Conv2D(kernel_size=(3, 3), filters=81, padding="same", activation='relu',
                                                 input_shape=input_shape))
        model.add(tensorflow.keras.layers.Conv2D(kernel_size=(3, 3), filters=81, padding="same", activation='relu'))
        model.add(tensorflow.keras.layers.Conv2D(kernel_size=(3, 3), filters=81, padding="same", activation='relu'))
        model.add(tensorflow.keras.layers.Flatten())
        model.add(tensorflow.keras.layers.Dense(729)) # BORROWED, represents sudoku grid and all possibilities of cells.
        model.add(tensorflow.keras.layers.Reshape((-1, 9)))  # BORROWED, reshapes our output to match our labels.
        model.add(tensorflow.keras.layers.Activation('softmax'))  # BORROWED,
        # converts the outputs to probabilities for each output.

        model.compile(loss='sparse_categorical_crossentropy',
                      optimizer=tensorflow.keras.optimizers.Adam(learning_rate=settings.learning_rate),
                      metrics=["accuracy"])

        self.model = model


