import random
import matplotlib.pyplot as plt
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

number_of_output_neurons = 3

number_of_epochs = 500
learning_rate = 0.01

# Ex 3.
def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def sigmoid_derivative(x):
    return sigmoid(x) * (1 - sigmoid(x))

def mse (actual_output, predicted_output):
    return np.mean((actual_output - predicted_output) ** 2)

def feed_forward(input, weights, bias):
    return sigmoid(np.dot(input, weights) + bias)


epoch_errors_to_plot = []
for epoch in range(1,number_of_epochs+1):
    epoch_error = 0
    for sample in date_antrenare:
        input = np.array([sample[0]])
        actual_output = np.zeros(number_of_output_neurons)
        actual_output[int(sample[1]) - 1] = 1
        layer1_output = feed_forward(input, weights_1, bias_1)
        layer2_output = feed_forward(layer1_output, weights_2, bias_2)
        output = feed_forward(layer2_output, weights_3, bias_3)
        epoch_error += mse(actual_output, output)
        
        gradients_3 = sigmoid_derivative(bias_3 + np.dot(layer2_output, weights_3)) * (actual_output - output)
        gradients_2 = sigmoid_derivative(bias_2 + np.dot(layer1_output, weights_2)) * np.dot(gradients_3, weights_3.T)
        gradients_1 = sigmoid_derivative(bias_1 + np.dot(input, weights_1)) * np.dot(gradients_2, weights_2.T)
        
        # print(gradients_1)
        # print(gradients_2)
        # print(gradients_3)
        weights_1 = weights_1 + learning_rate * np.dot(input.T, gradients_1)
        weights_2 = weights_2 + learning_rate * np.dot(layer1_output.T, gradients_2)
        weights_3 = weights_3 + learning_rate * np.dot(layer2_output.T, gradients_3)
        
        bias_1 = bias_1 + learning_rate * gradients_1
        bias_2 = bias_2 + learning_rate * gradients_2
        bias_3 = bias_3 + learning_rate * gradients_3
        
    epoch_errors_to_plot.append(epoch_error)
        
    if(epoch % 50 == 0):
        print(f"Epoch {epoch} completed. Error: {epoch_error}") 
        
plt.plot(range(1, number_of_epochs+1), epoch_errors_to_plot, label="Training Error")
plt.xlabel('Epoch')
plt.ylabel('Error')
plt.title('Training Error over Epochs')
plt.legend()
plt.show()
        



correct = []
wrong = []
for sample in date_testare:
    input = np.array([sample[0]])
    actual_output = np.zeros(number_of_output_neurons)
    actual_output[int(sample[1]) - 1] = 1
    layer1_output = feed_forward(input, weights_1, bias_1)
    layer2_output = feed_forward(layer1_output, weights_2, bias_2)
    #print(layer2_output)
    output = feed_forward(layer2_output, weights_3, bias_3)
    #print(output)
 
    if (actual_output[np.argmax(output)] == 1):
        print(f"Predicted: {np.argmax(output) + 1} Actual: {actual_output} " + "Corect")
        correct.append(sample)
    else:
        print(f"Predicted: {np.argmax(output) + 1} Actual: {actual_output} " + "Gresit") 
        wrong.append(sample)


print(f"Accuracy: {len(correct) / len(date_testare)}")
plt.plot([x[0][0] for x in correct], [x[0][1] for x in correct], 'go', label="Corect")
plt.plot([x[0][0] for x in wrong], [x[0][1] for x in wrong], 'ro', label="Gresit")
plt.xlabel('Atribute 1')
plt.ylabel('Atribute 2')
plt.title('Corect vs Gresit')
plt.legend()
plt.show()
