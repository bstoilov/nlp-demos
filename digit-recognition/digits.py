from mnist import MNIST
import matplotlib.pyplot as plt
import numpy as np
from keras.models import Sequential
from keras.layers.core import Dense
from keras.models import load_model
import os

image_size = 28
mnist_data_root = "/home/kashon/projects/Social-AI/tensorflow/data"
model_home = "../models/"
model_name = "digits"
full_model_file = model_home + model_name

if not os.path.exists(model_home):
    os.mkdir(model_home)



def plot_numbers(first_n=5):
    mndata = MNIST(mnist_data_root)
    images, labels = mndata.load_testing()

    plt.set_cmap('binary')
    for i in range(0, first_n):
        data = np.array(images[i], "float32")
        data = data.reshape(1, image_size, image_size, 1)
        image = np.asarray(data).squeeze()
        plt.imshow(image)
        plt.show()


def plot_pixels(img):
    plt.set_cmap('binary')
    data = np.array(img, "float32")
    data = data.reshape(1, image_size, image_size, 1)
    image = np.asarray(data).squeeze()
    plt.imshow(image)
    plt.show()


def get_train_data():
    mndata = MNIST(mnist_data_root)

    images, labels = mndata.load_training()
    output = []
    for l in labels:
        empty_in = [0] * 10
        empty_in[l % 10] = 1
        output.append(empty_in)

    return images, output


def get_test_data():
    mndata = MNIST(mnist_data_root)

    images, labels = mndata.load_testing()

    input = images
    output = []
    for l in labels:
        empty_in = [0] * 10
        empty_in[l % 10] = 1
        output.append(empty_in)

    return input, output


def train():
    model = Sequential()
    model.add(Dense(512, input_dim=image_size * image_size, activation='relu'))
    model.add(Dense(256, input_dim=512, activation='relu'))
    model.add(Dense(128, input_dim=256, activation='relu'))
    model.add(Dense(10, activation='sigmoid'))

    model.compile(loss='binary_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])

    training_data, target_data = get_train_data()

    training_data = np.array(training_data, "float32")
    target_data = np.array(target_data, "float32")

    model.fit(training_data, target_data, epochs=5, verbose=2)
    model.save(full_model_file)


def arr_to_num(arr):
    i = 0
    while i < len(arr):
        if arr[i] == 1:
            return i
        i += 1
    return 0


def test():
    test_data, expected_data = get_test_data()
    print(full_model_file)
    model = load_model(full_model_file)

    test_data_array = np.array(test_data, "float32")
    predictions = model.predict(test_data_array).round()

    print(len(test_data))

    for i in range(0, len(test_data)):
        predNum = arr_to_num(expected_data[i])  # expected number
        expt_num = arr_to_num(predictions[i])  # predicted number
        if predNum != expt_num:
            # print only when the network is wrong
            print('Actual: ' + str(predNum) + " Expected: " + str(expt_num))
            plot_pixels(test_data[i])


# train()

# plot_numbers()

test()
