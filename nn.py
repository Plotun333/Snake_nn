from matrix import Matrix
import math
import random


def sigmoid(num):
    return 1 / (1 + math.exp(-num))


def dsigmoid(num):
    return num * (1-num)


class NeuralNetwork(object):
    def __init__(self, input_nodes, hidden_nodes, output_nodes):

        self.outputs_hidden = []

        self.input_nodes = input_nodes
        self.output_nodes = output_nodes
        self.hidden_nodes = hidden_nodes

        self.hidden_weights = []
        self.hidden_biases = []

        index = 0

        self.hidden_weights.append(Matrix(self.hidden_nodes[0], self.input_nodes))
        self.hidden_biases.append(Matrix(self.hidden_nodes[0], 1))

        for element in self.hidden_nodes:
            if index == len(self.hidden_nodes)-1:
                self.hidden_weights.append(Matrix(self.output_nodes, element))
                self.hidden_biases.append(Matrix(self.output_nodes, 1))
            else:
                nex = self.hidden_nodes[index+1]
                self.hidden_weights.append(Matrix(nex, element))
                self.hidden_biases.append(Matrix(nex, 1))

            index += 1

        for weight in self.hidden_weights:
            weight.randomize()


        for bias in self.hidden_biases:
            bias.randomize()




    def feed_forward(self, input_array):
        inputs = Matrix.from_array(input_array)

        hidden = Matrix.multiply(self.hidden_weights[0], inputs)
        hidden = Matrix.add(hidden, self.hidden_biases[0])
        hidden = Matrix.map(hidden, sigmoid)
        self.outputs_hidden.append(hidden)

        index = 0
        for weight in self.hidden_weights:
            if index != 0 and index != len(self.hidden_weights)-1:

                hidden = Matrix.multiply(weight, hidden)
                hidden = Matrix.add(hidden, self.hidden_biases[index])
                hidden = Matrix.map(hidden, sigmoid)
                self.outputs_hidden.append(hidden)

            index += 1

        output = Matrix.multiply(self.hidden_weights[len(self.hidden_weights)-1], hidden)
        output = Matrix.add(output, self.hidden_biases[len(self.hidden_weights)-1])
        output = Matrix.map(output, sigmoid)
        self.outputs_hidden.append(output)

        return output.to_Array()

    def train(self, input_array, target_array, learning_rate=0.01):

        inputs = Matrix.from_array(input_array)

        #added
        weights_ih = self.hidden_weights[0]
        bias_h = self.hidden_biases[0]

        hidden = Matrix.multiply(weights_ih, inputs)
        hidden = Matrix.add(hidden, bias_h)

        hidden = Matrix.map(hidden, sigmoid)

        #added
        weights_ho = self.hidden_weights[1]
        bias_o = self.hidden_biases[1]

        outputs = Matrix.multiply(weights_ho, hidden)
        outputs = Matrix.add(outputs, bias_o)
        outputs = Matrix.map(outputs, sigmoid)


        targets = Matrix.from_array(target_array)


        output_errors = Matrix.subtract(targets, outputs)


        #gradient = outputs * (1 - outputs)

        gradients = Matrix.map(outputs, dsigmoid)
        gradients = Matrix.multiply( gradients,output_errors)
        gradients.multiply_to(learning_rate)

        hidden_T = Matrix.transpose(hidden)

        weight_ho_deltas = Matrix.multiply(gradients, hidden_T)

        weights_ho = Matrix.add(weights_ho, weight_ho_deltas)

        bias_o = Matrix.add(bias_o, gradients)


        who_t = Matrix.transpose(weights_ho)

        hidden_errors = Matrix.multiply(who_t, output_errors)


        hidden_gradient = Matrix.map(hidden,dsigmoid)
        hidden_gradient = Matrix.multiply(hidden_gradient, hidden_errors)
        hidden_gradient.multiply_to(learning_rate)


        inputs_T = Matrix.transpose(inputs)

        weight_ih_deltas = Matrix.multiply(hidden_gradient, inputs_T)

        weights_ih = Matrix.add(weights_ih, weight_ih_deltas)
        bias_h = Matrix.add(bias_h, hidden_gradient)

        self.hidden_weights[0] = weights_ih
        self.hidden_biases[0] = bias_h

        self.hidden_weights[1] = weights_ho
        self.hidden_biases[1] = bias_o


nn = NeuralNetwork(2, [2], 1)
inputs = [[1, 0], [0, 1], [1, 1], [0, 0]]
target = [[1], [1], [0], [0]]

for _ in range(100000):
    r = random.randint(0, 3)
    nn.train(inputs[r], target[r])


print(nn.feed_forward(inputs[0]))
print(nn.feed_forward(inputs[1]))
print(nn.feed_forward(inputs[2]))
print(nn.feed_forward(inputs[3]))
