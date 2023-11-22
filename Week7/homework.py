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

for epoch in range(number_of_epochs):
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
        
        bias_1 = bias_1 + learning_rate * np.sum(gradients_1, axis=0, keepdims=True)
        bias_2 = bias_2 + learning_rate * np.sum(gradients_2, axis=0, keepdims=True)
        bias_3 = bias_3 + learning_rate * np.sum(gradients_3, axis=0, keepdims=True)
        
    if(epoch % 50 == 0):
        print(f"Epoch {epoch} completed. Error: {epoch_error}") 
        



corecte = 0
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
        corecte +=1
    else:
        print(f"Predicted: {np.argmax(output) + 1} Actual: {actual_output} " + "Gresit") 

# for some reason mereu cand il rulezi o sa ai acc diferita ptt ca vad
# ca tine f mult de cum is randomizate datele la inceput adica uneori
# se poate antrena mai bine ,alteori mai prost , caz in care prob ar trb un nr de epoci mai mare  
# Gen are cazuri cand eroarea abia scade si acolo o sa fie probleme
# si cazuri in care scade mult si calculeaza mai bine weighturile si biasurile    

## incearca sa rulezi de mai multe ori si o sa vezi ca uneori e totu ok, alteori nu i asa buna acuratetea dar in mare cazuri
# la mine ( in majoritatea cazurilor) acuratetea e >0.7


# sterge comentariile astea dupa ce ai citit
print(f"Accuracy: {corecte / len(date_testare)}")