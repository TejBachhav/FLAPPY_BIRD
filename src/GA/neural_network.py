import numpy as np

class NeuralNetwork:
    def __init__(self, weights=None):
        # Architecture: 4 inputs, 5 hidden neurons, 1 output
        self.input_size = 4
        self.hidden_size = 5
        self.output_size = 1
        if weights is None:
            self.W1 = np.random.randn(self.hidden_size, self.input_size)
            self.b1 = np.random.randn(self.hidden_size)
            self.W2 = np.random.randn(self.output_size, self.hidden_size)
            self.b2 = np.random.randn(self.output_size)
        else:
            self.from_vector(weights)
    
    def from_vector(self, vec):
        vec = np.array(vec)
        end_W1 = self.hidden_size * self.input_size
        self.W1 = vec[:end_W1].reshape(self.hidden_size, self.input_size)
        end_b1 = end_W1 + self.hidden_size
        self.b1 = vec[end_W1:end_b1]
        end_W2 = end_b1 + self.output_size * self.hidden_size
        self.W2 = vec[end_b1:end_W2].reshape(self.output_size, self.hidden_size)
        self.b2 = vec[end_W2:]
    
    def to_vector(self):
        return np.concatenate((self.W1.flatten(), self.b1, self.W2.flatten(), self.b2))
    
    def forward(self, inputs):
        inputs = np.array(inputs)
        hidden = np.tanh(np.dot(self.W1, inputs) + self.b1)
        output = np.dot(self.W2, hidden) + self.b2
        # Sigmoid activation for output between 0 and 1
        return 1 / (1 + np.exp(-output))
