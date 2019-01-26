import h5py
import numpy as np
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras import optimizers
from keras.models import load_model
from keras.callbacks import ModelCheckpoint
import keras

from modules.controller.commands.module import Module
from modules.view.output_service import OutputService
from modules.shared.configurations import Configurations


##  This class handles the training of the neural network
class TrainingModule:

    __output_service: OutputService = OutputService()

    # Saving path and name
    __default_saving_path: str = Configurations.get_config(Module.TRAIN, "default_saving_path")
    __default_saving_name: str = Configurations.get_config(Module.TRAIN, "default_saving_name")

    # Network Structure:
    __num_conv_lavers: int = Configurations.get_config(Module.TRAIN, "num_conv_layers")
    __num_dense_layers: int = Configurations.get_config(Module.TRAIN, "num_dense_layers")
    __layer_activation: str = Configurations.get_config(Module.TRAIN, "layer_activation")
    __final_activation: str = Configurations.get_config(Module.TRAIN, "final_activation")
    __dropout: bool = Configurations.get_config(Module.TRAIN, "dropout")
    __num_classes: int = 5

    # Hyper parameters:
    __batch_size: int = Configurations.get_config(Module.TRAIN, "batch_size")
    __training_test_split: float = Configurations.get_config(Module.TRAIN, "training_test_split")
    __learning_rate: float = Configurations.get_config(Module.TRAIN, "learning_rate")
    __loss: str = Configurations.get_config(Module.TRAIN, "loss")


    ##  trains the neural network labeled matrices
    #
    #   @param matrices_path path where the labeled matrices are located
    #   @param neural_network_path path where are existing neural network is located if you want to improve one
    #   @param name under which the trained network will be saved
    #   @param saving_path path to where the trained network will be saved
    @staticmethod
    def train(matrices_path: str, neural_network_path: str, name: str, saving_path: str) -> None:

        # model is defined by the config file or loaded from a path
        model = TrainingModule.__define_model(neural_network_path)

        datagen = ImageDataGenerator()

        # loads matrices and labels from hdf5 file
        dataset = h5py.File(matrices_path, 'r')

        # converts matrices and labels in keras conform shape (samples, height, width, channels)
        matrices = np.expand_dims(np.array(dataset['dense_matrices']), axis=3)
        labels = np.array(dataset['label_vectors'])

        # saves model after every training epoch in format "saving_path+name+epochnr+loss"
        if saving_path == "" or saving_path is None: saving_path = TrainingModule.__default_saving_path
        if name == "" or name is None: name = TrainingModule.__default_saving_name
        checkpointer = ModelCheckpoint(filepath=saving_path + name + "{epoch:02d}-{loss:.2f}.hdf5", monitor='loss',
                                       verbose=1, save_best_only=True, save_weights_only=False, mode='auto', period=1)

        # trains model
        model.fit_generator(datagen.flow(matrices, labels, batch_size=TrainingModule.__batch_size),
                            steps_per_epoch=len(matrices) / TrainingModule.__batch_size,
                            epochs=5, callbacks=[checkpointer], verbose=1)
        model.summary()

    @staticmethod
    def __define_model(neural_network_path: str) -> keras.models.Sequential:
        if not neural_network_path or neural_network_path == "":
            model = Sequential()
            output_size = 32
            kernel_size = 3
            new_output_size = 0

            if TrainingModule.__num_conv_lavers != 0:
                model.add(Conv2D(output_size, (kernel_size, kernel_size), input_shape=(128, 128, 1)))
                model.add(Activation(TrainingModule.__layer_activation))
                new_output_size = output_size

            for i in range(1, TrainingModule.__num_conv_lavers):
                model.add(Conv2D(output_size * (i + 1), (kernel_size, kernel_size)))
                model.add(Activation(TrainingModule.__layer_activation))
                new_output_size = output_size * (i + 1)
            if TrainingModule.__dropout:
                model.add(Dropout(0.1))
            model.add(Flatten())

            if TrainingModule.__num_dense_layers > 1:
                model.add(Dense(new_output_size * 4))
                model.add(Activation(TrainingModule.__layer_activation))
                for i in range(1, TrainingModule.__num_dense_layers - 1):
                    model.add(Dense(int((new_output_size * 4) / i)))
                    model.add(Activation(TrainingModule.__layer_activation))
            model.add(Dense(TrainingModule.__num_classes))
            model.add(Activation(TrainingModule.__final_activation))

            optimizer = optimizers.SGD(lr=TrainingModule.__learning_rate)
            model.compile(loss=TrainingModule.__loss,
                          optimizer=optimizer, metrics=['accuracy'])
        else:
            # loads a compiled model from the specified path
            model = load_model(neural_network_path)

        return model

    @staticmethod
    def set_output_service(service: OutputService):
        TrainingModule.__output_service = service
