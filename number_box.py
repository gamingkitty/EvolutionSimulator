import pygame


def draw_text(screen, font, text, location, color=(255, 255, 255)):
    generated_text = font.render(text, True, color)
    screen.blit(generated_text, (location[0] - generated_text.get_rect().size[0]/2, location[1] - generated_text.get_rect().size[1]/2))


class NumberBox:
    def __init__(self, location, size, color, text_color, font):
        self.rect = pygame.rect.Rect(location, size)
        self.background = pygame.surface.Surface(size)
        self.background.fill(color)
        self.size = size
        self.color = color
        self.font = font
        self.text_color = text_color
        self.text = ""
        self.is_selected = False

    def load(self, screen):
        self.background.fill(self.color)
        draw_text(self.background, self.font, self.text, (self.size[0]/2, self.size[1]/2), self.text_color)
        screen.blit(self.background, self.rect)

    def get_number(self):
        return int(self.text)

    def handle_keypress(self, event):
        if self.is_selected:
            if event.key == pygame.K_BACKSPACE and self.text != "":
                self.text = self.text[:-1]
            elif event.key != pygame.K_BACKSPACE:
                self.text += event.unicode
