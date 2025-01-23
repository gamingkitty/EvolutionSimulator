import pygame


class Slider:
    def __init__(self, size, location, background_color, slider_color):
        self.background_rect = pygame.rect.Rect((0, 0), size)
        self.background_rect.centerx = location[0]
        self.background_rect.centery = location[1]
        self.slider_rect = pygame.rect.Rect((0, 0), (size[1] * 1.2, size[1] * 1.2))
        self.slider_rect.centerx = location[0]
        self.slider_rect.centery = location[1]
        self.background = pygame.Surface(size)
        self.background.fill(background_color)
        self.slider = pygame.Surface((size[1] * 1.2, size[1] * 1.2))
        self.slider.fill(slider_color)
        self.held = False

    def load(self, screen):
        screen.blit(self.background, self.background_rect)
        screen.blit(self.slider, self.slider_rect)

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.background_rect.collidepoint(mouse_pos):
            self.held = True
        if self.held:
            self.slider_rect.centerx = min(max(mouse_pos[0], self.background_rect.x), self.background_rect.topright[0])

    def get_value(self):
        return (self.slider_rect.centerx - self.background_rect.centerx) / self.background_rect.width
