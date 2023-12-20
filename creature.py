import numpy as np


# Note: Experiment with different activation functions
# Change to tanh possibly because with few neurons it seems that ReLU can output 0
# a lot and make it so that everything in the end is a zero.
# ReLU activation function for neural network.
def relu(x):
    return max(0, x)


# ReLU but applied to an entire list.
def vectorized_relu(x):
    return np.vectorize(relu)(x)


# Softmax activation function for last layer in neural network.
def softmax(x):
    exp_x = np.exp(x - np.max(x))
    return exp_x / exp_x.sum(axis=0, keepdims=True)


# Lists of all the sensory neurons and output neurons. These will be connected
# with weights and internal neurons. It is the same for all of the creatures, only weights differ.
# In order to add a new action or sense you need to add the neuron types name to this list, and also
# add its functionality to the act and sense functions above.
sensory_neuron_list = np.array(["x_coordinate", "y_coordinate", "time"])
output_neuron_list = np.array(["move_up", "move_down", "move_left", "move_right"])


class Creature:
    def __init__(self, internal_neuron_number):
        self.sensory_to_internal_weights = np.random.rand(internal_neuron_number, len(sensory_neuron_list)) - 0.5
        self.internal_to_output_weights = np.random.rand(len(output_neuron_list), internal_neuron_number) - 0.5

        self.x_coordinate = 1
        self.y_coordinate = 1

    # This function senses things about the creature and returns them for the neural
    # network to use as input. The neuron type refers to what information is to be
    # returned. This will always return a number.
    def sense(self, neuron_type):
        if neuron_type == "x_coordinate":
            return self.x_coordinate
        elif neuron_type == "y_coordinate":
            return self.y_coordinate
        elif neuron_type == "time":
            # Implement time here.
            return 1

    # This function calculates what the creature wants based on sensory neuron inputs and
    # then returns the move as a string.
    def move(self):
        # Input for neural network basically, applying sense function to all sensory neurons.
        move = np.vectorize(self.sense)(sensory_neuron_list)

        # Apply weights and activation function to the input
        move = vectorized_relu(np.dot(self.sensory_to_internal_weights, move))
        move = vectorized_relu(np.dot(self.internal_to_output_weights, move))

        # Apply softmax function to the final array of numbers.
        move = softmax(move)

        # Get a string name to return for an action to make.
        move = output_neuron_list[np.argmax(move)]
        return move
