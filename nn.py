from matrix import Matrix


class NeuralNetwork(object):
    def __init__(self, input_nodes, hidden_nodes, output_nodes):
        self.input_nodes = input_nodes
        self.hidden_nodes = hidden_nodes
        self.output_nodes = output_nodes
        self.weights_ih = Matrix(self.hidden_nodes, self.input_nodes)
        self.weights_ho = Matrix(self.output_nodes, self.hidden_nodes)
        self.weights_ih.randomize()
        self.weights_ho.randomize()
        self.bias_h = Matrix(self.hidden_nodes, 1)
        self.bias_o = Matrix(self.output_nodes, 1)



    def feedFoward(self, input_array):

        input = Matrix
        hidden = Matrix.multiply(self.weights_ih, input)
        hidden.add_to(self.bias_h)

