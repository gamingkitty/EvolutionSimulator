import pygame


class Button:
    def __init__(self, location, function, image):
        self.image = image
        self.rect = pygame.rect.Rect(location, self.image.get_size())
        self.function = function

    def is_hovering(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())

    def execute(self, global_vars):
        if self.function == "pause":
            global_vars["paused"] = not global_vars["paused"]

    def load(self, screen):
        screen.blit(self.image, self.rect)
