import sys
import numpy as np
import creature


# Combines all creatures together into a world to simulate evolution. Creatures are allowed to be on the same tile.
class World:
    # Defaults: learning_rate: 0.01, steps_to_reset: 100, creature_num: 100, creature_internal_neuron_num: 3
    def __init__(self, size_x, size_y):
        # The world is centered around an origin of 0, 0, so the size of the world will really be double that of
        # self.size_x and self.size_y, as the world includes both negative and positive coordinates.
        self.size_x = size_x
        self.size_y = size_y
        self.step_count = 0
        self.generations = 0
        self.last_generation_survived = 0

        self.creature_number = 0
        self.creature_internal_neuron_number = 0
        self.creatures = None
        self.set_creature_parameters()

        self.learning_rate = 0
        self.steps_to_reset = 0
        self.mutation_chance = 0
        self.set_evolution_parameters()

        # Moves every creature in a given list.
        self.step_creatures = np.vectorize(self.creature_step)
        # self.mutate_creatures = np.vectorize(lambda creature_obj: creature_obj.mutate(self.learning_rate))

    # Function that contains everything needed for 1 step in a creatures life cycle.
    def creature_step(self, creature_obj):
        creature_obj.move(self)

    # Simulate evolution for a given number of steps. Takes in the number of steps and a survival condition to check
    # if a given creature survives.
    def evolve(self, steps, survival_condition):
        for i in range(steps):
            self.step_creatures(self.creatures)
            self.step_count += 1
            if self.step_count >= self.steps_to_reset:
                surviving_creatures = np.array([creature_obj for creature_obj in self.creatures if survival_condition(creature_obj)])
                if len(surviving_creatures) == 0:
                    print("The creatures went extinct as every one of them died this generation.")
                    sys.exit()
                read_index = 0
                for x in range(self.creature_number):
                    self.creatures[x] = creature.Creature(0, 0, 0, surviving_creatures[read_index], True, self.learning_rate, self.mutation_chance)
                    self.creatures[x].randomize_coordinates(self.size_x, self.size_y)
                    self.creatures[x].steps = 0
                    read_index += 1
                    if read_index >= len(surviving_creatures):
                        read_index = 0
                self.last_generation_survived = len(surviving_creatures)
                self.step_count = 0
                self.generations += 1

    # Sets the evolution parameters, do this before evolution to customize it to your liking.
    # Takes in learning rate, and steps to reset
    def set_evolution_parameters(self, learning_rate=0.01, steps_to_reset=100, mutation_chance=0):
        self.learning_rate = learning_rate
        self.steps_to_reset = steps_to_reset
        self.mutation_chance = mutation_chance

    # Sets parameters for creatures, do this to customize the creatures.
    # Takes in creature number and the number of internal neurons for the creatures.
    def set_creature_parameters(self, creature_number=100, creature_internal_neuron_number=3):
        self.creature_number = creature_number
        self.creature_internal_neuron_number = creature_internal_neuron_number
        self.reset_creatures()

    # Resets every creature's brain and position. This will update creatures to any parameter changes during
    # evolution
    def reset_creatures(self):
        self.creatures = np.array(
            [creature.Creature(self.creature_internal_neuron_number, np.random.randint(-self.size_x, self.size_x),
                               np.random.randint(-self.size_y, self.size_y)) for _ in range(self.creature_number)])
