from matrix import Matrix
import math


def sigmoid(num):
    return 1 / (1 + math.exp(-num))


class NeuralNetwork(object):
    def __init__(self, input_nodes, hidden_nodes, output_nodes):
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
        hidden.map(sigmoid)

        index = 0
        for weight in self.hidden_weights:
            if index != 0 and index != len(self.hidden_weights)-1:

                hidden = Matrix.multiply(weight, hidden)
                hidden = Matrix.add(hidden, self.hidden_biases[index])
                hidden.map(sigmoid)

            index += 1

        output = Matrix.multiply(self.hidden_weights[len(self.hidden_weights)-1], hidden)
        output = Matrix.add(output, self.hidden_biases[len(self.hidden_weights)-1])
        output.map(sigmoid)

        return output.to_Array()


nn = NeuralNetwork(1, [1], 1)

print(nn.feed_forward([1]))
