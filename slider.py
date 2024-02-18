import pygame


class Slider:
    def __init__(self, size, location, background_color, slider_color):
        self.background_rect = pygame.rect.Rect(location, size)
        self.slider_rect = pygame.rect.Rect((location[0] + size[0]/2, location[1] + size[1]/2), (size[1] * 1.2, size[1] * 1.2))
        self.background = pygame.Surface(size)
        self.background.fill(background_color)
        self.slider = pygame.Surface((size[1] * 1.2, size[1] * 1.2))
        self.slider.fill(slider_color)

    def load(self, screen):
        screen.blit(self.background, self.background_rect)
        screen.blit(self.slider, self.slider_rect)
