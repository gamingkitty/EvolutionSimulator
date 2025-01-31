import numpy as np


# It seems that ReLU can output 0
# a lot and make it so that everything in the end is a zero.
# ReLU activation function for neural network.
def relu(x):
    return max(0, x)


# Modifies a numpy array of any shape/size randomly. Modifies the fraction within the given magnitude. Modifies
# by adding a random number to the random elements selected.
def modify_random_elements(arr, fraction=0.1, magnitude=0.5):
    # Flatten the array to 1D
    flattened_arr = arr.ravel()

    # Get the number of elements to modify
    num_elements = int(flattened_arr.size * fraction)

    # Generate random indices
    random_indices = np.random.choice(flattened_arr.size, num_elements, replace=False)

    # Generate random values within the specified range
    random_values = np.random.uniform(-magnitude, magnitude, num_elements)

    # Modify the random elements
    np.add.at(flattened_arr, random_indices, random_values)

    # Reshape the array back to its original shape
    arr[:] = flattened_arr.reshape(arr.shape)


# These functions are stored in variables to make them more efficient, as they are called many times.
# ReLU but applied to an entire list.
vectorized_relu = np.vectorize(relu, [float])


# Hyperbolic tangent activation function.
vectorized_tanh = np.vectorize(np.tanh, [float])


# Softmax activation function for last layer in neural network.
def softmax(x):
    exp_x = np.exp(x - np.max(x))
    return exp_x / exp_x.sum(axis=0, keepdims=True)


# Lists of all the sensory neurons and output neurons. These will be connected
# with weights and internal neurons. It is the same for all the creatures, only weights differ.
# In order to add a new action or sense you need to add the neuron types name to this list, and also
# add its functionality to the sense function.
sensory_neuron_list = np.array(["x_coordinate", "y_coordinate", "time", "bias", "oscillating"])
output_neuron_list = np.array(["move_up", "move_down", "move_left", "move_right", "nothing"])

# The activation function used in the neural network.
ACTIVATION_FUNCTION = vectorized_tanh


# Creature class, stores a creature, which includes its neural network and position.
class Creature:
    def __init__(self, internal_neuron_number, starting_x, starting_y, create_from=None, mutate=False, learning_rate=0, chance_to_mutate=100):
        # Copy everything from another creature during initialization
        if create_from is not None:
            self.sensory_to_internal_weights = np.copy(create_from.sensory_to_internal_weights)
            self.internal_to_output_weights = np.copy(create_from.internal_to_output_weights)

            self.x_coordinate = create_from.x_coordinate
            self.y_coordinate = create_from.y_coordinate
            self.steps = create_from.steps
            self.color = create_from.color
            if mutate and chance_to_mutate == 100:
                self.mutate(learning_rate)
            elif mutate and np.random.randint(0, 100) < chance_to_mutate:
                self.mutate(learning_rate)
        else:
            self.sensory_to_internal_weights = np.random.rand(internal_neuron_number, len(sensory_neuron_list)) - 0.5
            self.internal_to_output_weights = np.random.rand(len(output_neuron_list), internal_neuron_number) - 0.5

            self.x_coordinate = starting_x
            self.y_coordinate = starting_y

            self.steps = 0

            self.color = (np.random.randint(0, 255), np.random.randint(0, 200), np.random.randint(0, 255))

        self.vectorized_sense = np.vectorize(self.sense, [float])

    # This function senses things about the creature and returns them for the neural
    # network to use as input. The neuron type refers to what information is to be
    # returned. This will always return a number.
    def sense(self, neuron_type):
        if neuron_type == "x_coordinate":
            return self.x_coordinate/100
        elif neuron_type == "y_coordinate":
            return self.y_coordinate / 100
        elif neuron_type == "time":
            return self.steps / 100
        elif neuron_type == "bias":
            return 1
        elif neuron_type == "oscillating":
            return np.sin(self.steps / 3)
        else:
            raise ValueError(f"Invalid neuron type {neuron_type} to sense for.")

    # This function calculates what the creature wants based on sensory neuron inputs and
    # then returns the move as a string.
    def get_move(self):
        # Input for neural network basically, applying sense function to all sensory neurons.
        move = self.vectorized_sense(sensory_neuron_list)

        # Apply weights and activation function to the input
        move = ACTIVATION_FUNCTION(np.dot(self.sensory_to_internal_weights, move))
        move = softmax(np.dot(self.internal_to_output_weights, move))
        # Get a string name to return for an action to make.
        move = output_neuron_list[np.argmax(move)]

        return move

    # For future: Possibly make it so that the creatures can interact with each other and more things in the world.
    # This function both gets the move from the neural network and then does the action based on that move.
    # If you want to implement more actions, you will implement their functionality here. Don't forget to also add the
    # neurons to the output neuron list too though.
    def move(self, world_obj, print_move=False):
        move = self.get_move()
        if print_move:
            print(move)

        if move == "move_up":
            self.y_coordinate += 1
        elif move == "move_down":
            self.y_coordinate -= 1
        elif move == "move_right":
            self.x_coordinate += 1
        elif move == "move_left":
            self.x_coordinate -= 1
        elif move != "nothing":
            raise ValueError(f"Move {move} outputted by neural network is not recognized as a valid move. You may have" +
                             f" added a neuron to the output list without implementing its function.")

        self.steps += 1
        self.normalize_coordinates(world_obj.size_x, world_obj.size_y)

    # Normalizes coordinates to a specific size, such that none of them can be greater than that size
    # or less than the negative of that size.
    def normalize_coordinates(self, world_size_x, world_size_y):
        if self.x_coordinate > world_size_x:
            self.x_coordinate = world_size_x
        elif self.x_coordinate < -world_size_x:
            self.x_coordinate = -world_size_x
        elif self.y_coordinate > world_size_y:
            self.y_coordinate = world_size_y
        elif self.y_coordinate < -world_size_y:
            self.y_coordinate = -world_size_y

    # Mutates the creatures weights using a learning rate to determine by how much. One way you could try and
    # modify the simulation to customize it is change the mutations, like how they work or the chances for different
    # mutations to happen.
    # Modify this so that it can set ones to 0 and it can also completely change weights instead of just adding or subtracting.
    def mutate(self, learning_rate, mutation_probability=0.1):
        # Modify the color of the creature
        new_red = self.color[0] + np.random.uniform(-100 * learning_rate, 100 * learning_rate)
        new_green = self.color[1] + np.random.uniform(-100 * learning_rate, 100 * learning_rate)
        new_blue = self.color[2] + np.random.uniform(-100 * learning_rate, 100 * learning_rate)
        new_red = min(max(new_red, 0), 255)
        new_green = min(max(new_green, 0), 200)  # Make sure that the creature is still visible on the background.
        new_blue = min(max(new_blue, 0), 255)
        self.color = (new_red, new_green, new_blue)

        def apply_mutation(weights):
            mutation_mask = np.random.rand(*weights.shape) < mutation_probability
            mutation_values = np.random.normal(loc=0.0, scale=learning_rate, size=weights.shape)
            return weights + mutation_mask * mutation_values

        # Apply mutations to the weights
        self.sensory_to_internal_weights = apply_mutation(self.sensory_to_internal_weights)
        self.internal_to_output_weights = apply_mutation(self.internal_to_output_weights)

    # Randomizes the coordinates of the creature within the constraints of a given size.
    def randomize_coordinates(self, world_size_x, world_size_y):
        self.x_coordinate = np.random.randint(-world_size_x, world_size_x)
        self.y_coordinate = np.random.randint(-world_size_y, world_size_y)
