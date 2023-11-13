
import random
import numpy as np

date_antrenare = []
date_testare = []

with open("seeds_dataset.txt", "r") as f:
    for line in f.readlines():
        line = line.strip()
        line = line.split()
        line = [float(x) for x in line]
        line = [line[:-1], line[-1]]
        date_antrenare.append(line)


random.shuffle(date_antrenare)
nr_testare = int(len(date_antrenare) * 0.2)
date_testare = date_antrenare[:nr_testare]
date_antrenare = date_antrenare[nr_testare:]


# Ex 2.
weights_1 = np.random.uniform(-1, 1, (7, 9))
weights_2 = np.random.uniform(-1, 1, (9, 5))
weights_3 = np.random.uniform(-1, 1, (5, 3))

bias_1 = np.random.uniform(-1, 1, (1, 9))
bias_2 = np.random.uniform(-1, 1, (1, 5))
bias_3 = np.random.uniform(-1, 1, (1, 3))

number_of_epochs = 500
learning_rate = 0.1


# Ex 3.
def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def sigmoid_derivative(x):
    return sigmoid(x) * (1 - sigmoid(x))


def error(output, expected):
    return np.power(output - expected, 2)


# Ex 4.


def feed_forward(input, weights, bias):
    return sigmoid(np.dot(input, weights) + bias)


for input in date_antrenare:
    output = feed_forward(input[0], weights_1, bias_1)
    output = feed_forward(output, weights_2, bias_2)
    output = feed_forward(output, weights_3, bias_3)
    print(output)
