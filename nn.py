from matrix import Matrix
import math
import random


class NeuralNetwork(object):
    def __init__(self, input_nodes=None, hidden_nodes=None, output_nodes=None):
        if isinstance(input_nodes, NeuralNetwork):
            nn = input_nodes

            self.outputs_hidden = nn.outputs_hidden
            self.input_nodes = nn.input_nodes
            self.output_nodes = nn.output_nodes
            self.hidden_nodes = nn.hidden_nodes
            self.hidden_weights = nn.hidden_weights
            self.hidden_biases = nn.hidden_biases
            self.activation_func = NeuralNetwork.sigmoid
        else:
            self.activation_func = NeuralNetwork.sigmoid
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
                if index == len(self.hidden_nodes) - 1:
                    self.hidden_weights.append(Matrix(self.output_nodes, element))
                    self.hidden_biases.append(Matrix(self.output_nodes, 1))
                else:
                    nex = self.hidden_nodes[index + 1]
                    self.hidden_weights.append(Matrix(nex, element))
                    self.hidden_biases.append(Matrix(nex, 1))

                index += 1

            for weight in self.hidden_weights:
                weight.randomize()

            for bias in self.hidden_biases:
                bias.randomize()

    # Activation functions
    @staticmethod
    def sigmoid(num):
        return 1 / (1 + math.exp(-num))

    @staticmethod
    def dsigmoid(num):
        return num * (1 - num)

    def feed_forward(self, input_array):
        inputs = Matrix.from_array(input_array)

        hidden = Matrix.multiply(self.hidden_weights[0], inputs)
        hidden = Matrix.add(hidden, self.hidden_biases[0])
        hidden = Matrix.map(hidden, self.activation_func)
        self.outputs_hidden.append(hidden)

        index = 0
        for weight in self.hidden_weights:
            if index != 0 and index != len(self.hidden_weights) - 1:
                hidden = Matrix.multiply(weight, hidden)
                hidden = Matrix.add(hidden, self.hidden_biases[index])
                hidden = Matrix.map(hidden, self.activation_func)
                self.outputs_hidden.append(hidden)

            index += 1

        output = Matrix.multiply(self.hidden_weights[len(self.hidden_weights) - 1], hidden)
        output = Matrix.add(output, self.hidden_biases[len(self.hidden_weights) - 1])
        output = Matrix.map(output, self.activation_func)
        self.outputs_hidden.append(output)

        return output.to_Array()

    # train can only work with a neural net with one hidden layer
    def train(self, input_array, target_array, learning_rate=0.1, epoch=50000, ran=False):
        print("!!!method train can only work with a neural net with one hidden layer!!!")
        if len(input_array) != len(target_array):
            print("!!! ERROR target list must have the same length as input list")
            return None
        index = 0
        progress = 0
        for procent in range(epoch):
            if index == len(input_array) - 1:
                index = 0
            if ran:
                index = random.randint(0, len(input_array) - 1)

            inputs = Matrix.from_array(input_array[index])
            # added
            weights_ih = self.hidden_weights[0]
            bias_h = self.hidden_biases[0]

            hidden = Matrix.multiply(weights_ih, inputs)
            hidden = Matrix.add(hidden, bias_h)
            hidden = Matrix.map(hidden, self.activation_func)

            weights_ho = self.hidden_weights[1]
            bias_o = self.hidden_biases[1]

            outputs = Matrix.multiply(weights_ho, hidden)
            outputs = Matrix.add(outputs, bias_o)
            outputs = Matrix.map(outputs, self.activation_func)

            targets = Matrix.from_array(target_array[index])

            output_errors = Matrix.subtract(targets, outputs)

            if progress / epoch >= 0.1:
                progress = 0
                print('Loading... ', procent / epoch * 100, '%')

            gradients = Matrix.map(outputs, self.dsigmoid)
            gradients = Matrix.multiply(gradients, output_errors)
            gradients.multiply_to(learning_rate)

            hidden_t = Matrix.transpose(hidden)

            weight_ho_deltas = Matrix.multiply(gradients, hidden_t)

            weights_ho = Matrix.add(weights_ho, weight_ho_deltas)

            bias_o = Matrix.add(bias_o, gradients)

            who_t = Matrix.transpose(weights_ho)

            hidden_errors = Matrix.multiply(who_t, output_errors)

            hidden_gradient = Matrix.map(hidden, self.dsigmoid)
            hidden_gradient = Matrix.multiply(hidden_gradient, hidden_errors)
            hidden_gradient.multiply_to(learning_rate)

            inputs_t = Matrix.transpose(inputs)

            weight_ih_deltas = Matrix.multiply(hidden_gradient, inputs_t)

            weights_ih = Matrix.add(weights_ih, weight_ih_deltas)
            bias_h = Matrix.add(bias_h, hidden_gradient)

            self.hidden_weights[0] = weights_ih
            self.hidden_biases[0] = bias_h

            self.hidden_weights[1] = weights_ho
            self.hidden_biases[1] = bias_o
            index += 1
            progress += 1
        print("Loading... finished")

    def copy(self):
        return NeuralNetwork(self)

    def mutate(self, rate):
        def mutate(val):
            if (random.randint(0, 100)/100) < rate:
                return (random.randint(0, 2000)/1000)-1
            else:
                return val
        weights_new = []
        biases_new = []
        for weight in self.hidden_weights:
            weight = Matrix.map(weight, mutate)
            weights_new.append(weight)

        for bias in self.hidden_biases:
            bias = Matrix.map(bias, mutate)
            biases_new.append(bias)

        self.hidden_weights = weights_new
        self.hidden_biases = biases_new

# XOR EXAMPLE
# nn = NeuralNetwork(2, [2], 1)
# inputs = [[1, 0], [0, 1], [1, 1], [0, 0]]
# target = [[1], [1], [0], [0]]


# r = random.randint(0, 3)
# nn.train(inputs, target, 0.01, 500000, True)


# print(nn.feed_forward(inputs[0]))
# print(nn.feed_forward(inputs[1]))
# print(nn.feed_forward(inputs[2]))
# print(nn.feed_forward(inputs[3]))
n = NeuralNetwork(2, [2], 2)
n2 = n.copy()
for i in n.hidden_weights:
    i.print()
print('\n')
n2.mutate(1)
for i in n2.hidden_weights:
    i.print()
