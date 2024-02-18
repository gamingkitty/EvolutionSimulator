import time
import numpy as np
import creature
import world
import pygame
import sys


# This is the survival condition for the creatures. It takes in a creature and returns a boolean. It returns true
# if the creature survives, and false if the creature dies.
def survival_condition(creature_obj):
    # return creature_obj.x_coordinate > 0
    return creature_obj.x_coordinate > 200 or creature_obj.x_coordinate < -200

# TODO: Implement system of fitness, replaces survival fitness with fitness function on a creature. More fitness means
#       offspring. Change mutations as well. Make it so it can set some weights to 0 in order to remove unnecessary connections.
#       And make sure to test the different chances and everything.


def draw_text(screen, font, text, location, color=(255, 255, 255)):
    generated_text = font.render(text, True, color)
    screen.blit(generated_text, (location[0] - generated_text.get_rect().size[0]/2, location[1] - generated_text.get_rect().size[1]/2))


# Main function, takes all the classes together and uses them to display and test the program so far.
def main():
    # Change this to false if the background image isn't working to turn off the background.
    generate_background_from_survival_function = True

    creature_num = 100
    creature_internal_neuron_num = 3
    creature_mutation_rate = 5
    learning_rate = 0.1
    steps_to_reset = 250

    world_x = 256
    world_y = 128

    creature_world = world.World(world_x, world_y)
    creature_world.set_creature_parameters(creature_num, creature_internal_neuron_num)
    creature_world.set_evolution_parameters(learning_rate, steps_to_reset, creature_mutation_rate)

    pygame.init()
    # This setting controls the size of the screen. It can be a non integer, but it might display a little weird.
    size_mult = 3

    screen_size = (creature_world.size_x * size_mult * 2 + size_mult, creature_world.size_y * size_mult * 2 + size_mult)
    screen = pygame.display.set_mode(screen_size)
    font = pygame.font.Font(None, 36)
    small_font = pygame.font.Font(None, 18)
    pygame.display.set_caption("Evolution Simulator")

    step_rate = 1
    paused = False

    # Initialize all the images here
    # Generate a background image according to the survival condition function. This only works if the survival condition
    # is based on x y coordinates, otherwise you can set "generate_background_image_from_survival_condition" to false.
    background_image = pygame.Surface(screen_size)
    background_image.fill((0, 0, 0))
    if generate_background_from_survival_function:
        for y in range((world_y * 2) + 1):
            for x in range((world_x * 2) + 1):
                if survival_condition(creature.Creature(0, x - world_x, y - world_y)):
                    pygame.draw.rect(background_image, (0, 255, 0), (x * size_mult, screen_size[1] - (y * size_mult) - size_mult, size_mult, size_mult))
    # Button images initialization.
    pause_button = pygame.image.load("buttons/PauseButton.png")
    play_button = pygame.image.load("buttons/PlayButton.png")
    settings_button = pygame.image.load("buttons/SettingsButton.png")
    slider_background = pygame.Surface((100, 16))
    slider_background.fill((80, 80, 80))
    slider_mover = pygame.Surface((20, 20))
    slider_mover.fill((255, 255, 255))
    slider_x = screen_size[0]/2 + 22
    dark_surface = pygame.Surface((screen_size[0], screen_size[1]))
    dark_surface.fill((0, 0, 0))
    dark_surface.set_alpha(128)
    mouse_held = False

    # Timers
    step_cd = 0
    step_timer = 0

    cur_screen = "main"

    # Main game loop
    while True:
        mouse_pos = pygame.mouse.get_pos()
        settings_button_hovered = settings_button.get_rect(topleft=(22 - settings_button.get_rect().size[0]/2, 22 - settings_button.get_rect().size[1]/2)).collidepoint(mouse_pos)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Handle button presses.
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if cur_screen == "main" and pause_button.get_rect(topleft=((screen_size[0])/2 - pause_button.get_rect().size[0]/2 - 58, 6)).collidepoint(mouse_pos):
                        paused = not paused
                        step_rate = 0
                    if settings_button_hovered:
                        if cur_screen != "settings":
                            cur_screen = "settings"
                        else:
                            cur_screen = "main"
                    mouse_held = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    mouse_held = False
        if cur_screen == "main":
            if mouse_held:
                if slider_background.get_rect(topleft=(screen_size[0]/2 - slider_background.get_rect().size[0]/2 + 22, 14)).collidepoint(mouse_pos):
                    slider_x = mouse_pos[0]
            if not paused:
                speed = round((slider_x - (screen_size[0]/2 + 22)) / 10)
                if speed >= 0:
                    step_rate = speed + 1
                    step_cd = 0
                else:
                    step_rate = 1
                    step_cd = -speed

        screen.blit(background_image, (0, 0))
        draw_text(screen, font, f"Generation {creature_world.generations}", (screen_size[0]/2, 50))
        draw_text(screen, small_font, f"Creatures survived last generation: {creature_world.last_generation_survived}/{creature_num}", (screen_size[0]/2, 70))
        if not paused:
            screen.blit(pause_button, ((screen_size[0])/2 - pause_button.get_rect().size[0]/2 - 58, 6))
        else:
            screen.blit(play_button, (screen_size[0]/2 - play_button.get_rect().size[0]/2 - 58, 6))

        if settings_button_hovered:
            settings_button.set_alpha(256)
        else:
            settings_button.set_alpha(128)
        screen.blit(slider_background, (screen_size[0]/2 - slider_background.get_rect().size[0]/2 + 22, 14))
        screen.blit(slider_mover, (slider_x - slider_mover.get_rect().size[0]/2, 12))

        for creature_obj in creature_world.creatures:
            # Draw a red square for every creature. Inverse y coordinates for displaying in the correct position.
            x, y = creature_obj.x_coordinate + world_x, world_y - creature_obj.y_coordinate
            pygame.draw.rect(screen, creature_obj.color, (x * size_mult, y * size_mult, size_mult, size_mult))
        if cur_screen == "main":
            if step_timer >= step_cd:
                creature_world.evolve(step_rate, survival_condition)
                step_timer = 0
            else:
                time.sleep(0.01)
                step_timer += 1
        elif cur_screen == "settings":
            screen.blit(dark_surface, (0, 0))
        screen.blit(settings_button, (22 - settings_button.get_rect().size[0]/2, 22 - settings_button.get_rect().size[1]/2))
        pygame.display.flip()


if __name__ == '__main__':
    main()
