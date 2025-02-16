import numpy as np

class NeuralNetwork:
    """
    A simple feedforward neural network with one hidden layer.
    
    Architecture:
        - Input layer: 4 neurons
        - Hidden layer: 5 neurons (tanh activation)
        - Output layer: 1 neuron (sigmoid activation)
    """
    def __init__(self, weights=None):
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
        """
        Initialize network parameters from a flat vector.
        """
        vec = np.array(vec)
        end_W1 = self.hidden_size * self.input_size
        self.W1 = vec[:end_W1].reshape(self.hidden_size, self.input_size)
        
        end_b1 = end_W1 + self.hidden_size
        self.b1 = vec[end_W1:end_b1]
        
        end_W2 = end_b1 + self.output_size * self.hidden_size
        self.W2 = vec[end_b1:end_W2].reshape(self.output_size, self.hidden_size)
        
        self.b2 = vec[end_W2:]
    
    def to_vector(self):
        """
        Flatten all network parameters into a single vector.
        """
        return np.concatenate((self.W1.flatten(), self.b1, self.W2.flatten(), self.b2))
    
    def forward(self, inputs):
        """
        Perform a forward pass through the network.
        
        Args:
            inputs (iterable): Input values (should be of length 4).
        
        Returns:
            The network's output after applying the sigmoid activation.
        """
        inputs = np.array(inputs)
        hidden = np.tanh(np.dot(self.W1, inputs) + self.b1)
        output = np.dot(self.W2, hidden) + self.b2
        # Apply sigmoid activation to the output
        return 1 / (1 + np.exp(-output))
