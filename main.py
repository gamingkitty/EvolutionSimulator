import math
import sys
import numpy as np
import pygame
import world
import creature
import button
import slider


def fitness_function(creature_obj):
    return max(100 - math.hypot(creature_obj.x_coordinate, creature_obj.y_coordinate), 0)


def draw_text(screen, font, text, location, color=(255, 255, 255)):
    generated_text = font.render(text, True, color)
    screen.blit(generated_text, (location[0] - generated_text.get_rect().size[0]/2, location[1] - generated_text.get_rect().size[1]/2))


def main():
    world_x = 256
    world_y = 128

    creature_num = 200
    creature_internal_neuron_num = 10
    creature_mutation_rate = 0.1
    learning_rate = 0.1
    steps_to_reset = 200
    steps_per_tick = 1

    # These shows the number of tiles that are actually within the world.
    modified_world_x = world_x * 2 + 1
    modified_world_y = world_y * 2 + 1

    # Changes how large the world shows up as visually.
    size_mult = 3

    creature_world = world.World(world_x, world_y)
    creature_world.set_creature_parameters(creature_num, creature_internal_neuron_num)
    creature_world.set_evolution_parameters(learning_rate, steps_to_reset, creature_mutation_rate)

    pygame.init()

    screen_size = (modified_world_x * size_mult, modified_world_y * size_mult)
    screen = pygame.display.set_mode(screen_size)

    pygame.display.set_caption("Evolution Simulator")

    clock = pygame.time.Clock()
    fps = 60

    # Visual things for UI
    black = (0, 0, 0)
    white = (255, 255, 255)
    green = (0, 255, 0)
    gray = (80, 80, 80)

    font = pygame.font.Font(None, 36)
    small_font = pygame.font.Font(None, 18)

    global_vars = {"paused": False}

    # Buttons
    pause_image = pygame.image.load("UI/PauseButton.png")
    play_image = pygame.image.load("UI/PlayButton.png")
    pause_button = button.Button((screen_size[0] / 2 - pause_image.get_size()[0] / 2 - 58, 6), "pause", pause_image)

    # Sliders
    speed_slider = slider.Slider((100, 16), (screen_size[0]/2 + 21, 21), gray, white)

    # Create the background image to show where creatures will die or where they will survive.
    background_image = pygame.Surface((modified_world_x, modified_world_y))
    background_image.fill(black)
    test_creature = creature.Creature(0, 0, 0)
    creature_fitness = np.zeros((modified_world_y, modified_world_x))
    for y in range(modified_world_y):
        for x in range(modified_world_x):
            test_creature.x_coordinate = x - world_x
            test_creature.y_coordinate = world_y - y
            creature_fitness[y][x] = fitness_function(test_creature)

    highest_fitness = np.max(creature_fitness)
    for y in range(modified_world_y):
        for x in range(modified_world_x):
            pygame.draw.rect(background_image, (0, (creature_fitness[y][x] * 255) / highest_fitness, 0), (x, y, 1, 1))
    background_image = pygame.transform.scale(background_image, screen_size)

    mouse_held = False

    while True:
        clock.tick(fps)
        screen.blit(background_image, (0, 0))
        if not global_vars["paused"]:
            creature_world.evolve(steps_per_tick, fitness_function)

        # Display the creatures.
        for creature_obj in creature_world.creatures:
            # Draw a square for every creature. Inverse y coordinates for displaying in the correct position.
            x, y = creature_obj.x_coordinate + world_x, world_y - creature_obj.y_coordinate
            pygame.draw.rect(screen, creature_obj.color, (x * size_mult, y * size_mult, size_mult, size_mult))

        if mouse_held:
            speed_slider.update()
            steps_per_tick = math.exp(6 * speed_slider.get_value())

        # Draw the UI
        draw_text(screen, font, f"Generation {creature_world.generations}", (screen_size[0] / 2, 50))
        draw_text(screen, small_font,
                  f"Creatures that reproduced last generation: {creature_world.last_generation_reproduced}/{creature_num}",
                  (screen_size[0] / 2, 70))

        pause_button.load(screen)
        speed_slider.load(screen)

        # Event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                if pause_button.is_hovering():
                    pause_button.execute(global_vars)
                    if global_vars["paused"]:
                        pause_button.image = play_image
                    else:
                        pause_button.image = pause_image
                mouse_held = False
                speed_slider.held = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_held = True

        pygame.display.flip()


if __name__ == "__main__":
    main()
