
import random
import math
date_antrenare = []
date_testare = []

with open("seeds_dataset.txt", "r") as f:
    for line in f.readlines():
        line = line.strip()
        line = line.split()
        line = [float(x) for x in line]
        date_antrenare.append(line)


random.shuffle(date_antrenare)
nr_testare = int(len(date_antrenare) * 0.2)
date_testare = date_antrenare[:nr_testare]
date_antrenare = date_antrenare[nr_testare:]

# now, for the next part we will train a neural netowork for forward propagation


def init_network(nr_inputs, nr_hidden, nr_outputs):
    network = []
    hidden_layer = [{'weights': [random.random() for i in range(nr_inputs + 1)]}
                    for i in range(nr_hidden)]
    network.append(hidden_layer)
    output_layer = [{'weights': [random.random() for i in range(nr_hidden + 1)]}
                    for i in range(nr_outputs)]
    network.append(output_layer)
    return network


def activate(weights, inputs):
    activation = weights[-1]
    for i in range(len(weights) - 1):
        activation += weights[i] * inputs[i]
    return activation


def transfer(activation):
    return 1.0 / (1.0 + math.exp(-activation))


def forward_propagate(network, row):
    inputs = row
    for layer in network:
        new_inputs = []
        for neuron in layer:
            activation = activate(neuron['weights'], inputs)
            neuron['output'] = transfer(activation)
            new_inputs.append(neuron['output'])
        inputs = new_inputs
    return inputs



# print("Date de antrenare: ", date_antrenare)
# print("Date de testare: ", date_testare)
network = init_network(7, 5, 3)
print("Network: ", network)
for row in date_antrenare:
    outputs = forward_propagate(network, row)
    print(outputs)
