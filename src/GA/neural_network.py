import numpy as np

def sigmoid(x):
    """Compute the sigmoid activation function."""
    return 1 / (1 + np.exp(-x))

def tanh(x):
    """Compute the hyperbolic tangent activation function."""
    return np.tanh(x)

class NeuralNetwork:
    """
    A configurable feedforward neural network with one hidden layer.
    
    Default Architecture:
        - Input layer: 4 neurons
        - Hidden layer: 5 neurons (using tanh activation)
        - Output layer: 1 neuron (using sigmoid activation)
    
    This network can be used as a controller for the GA simulation.
    
    Args:
        weights (array-like, optional): A flat vector of weights to initialize the network.
        input_size (int, optional): Number of input neurons. Default is 4.
        hidden_size (int, optional): Number of neurons in the hidden layer. Default is 5.
        output_size (int, optional): Number of output neurons. Default is 1.
    """
    def __init__(self, weights=None, input_size=4, hidden_size=5, output_size=1):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        
        if weights is None:
            # Initialize weights and biases from a normal distribution.
            self.W1 = np.random.randn(self.hidden_size, self.input_size)
            self.b1 = np.random.randn(self.hidden_size)
            self.W2 = np.random.randn(self.output_size, self.hidden_size)
            self.b2 = np.random.randn(self.output_size)
        else:
            self.from_vector(weights)
    
    def from_vector(self, vec):
        """
        Initialize network parameters from a flat vector.
        
        Args:
            vec (iterable): A flat vector containing all network weights and biases.
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
        
        Returns:
            np.ndarray: A 1D array containing all weights and biases.
        """
        return np.concatenate((self.W1.flatten(), self.b1, self.W2.flatten(), self.b2))
    
    def forward(self, inputs):
        """
        Perform a forward pass through the network.
        
        Args:
            inputs (iterable): Input values (must have length equal to input_size).
        
        Returns:
            np.ndarray: The network's output after applying activations.
        """
        inputs = np.array(inputs)
        hidden = tanh(np.dot(self.W1, inputs) + self.b1)
        output = np.dot(self.W2, hidden) + self.b2
        return sigmoid(output)
    
    def predict(self, inputs):
        """
        Alias for the forward pass. Returns the network's output.
        
        Args:
            inputs (iterable): Input values.
        
        Returns:
            np.ndarray: The network's output.
        """
        return self.forward(inputs)
