import pygame.font


class Menu:
    def __init__(self, font: pygame.font.Font) -> None:
        self.options = []
        self.curr_option = 0
        self.font = font

    def add_option(self, option, callback) -> None:
        self.options.append((option, callback))

    def select(self) -> None:
        self.options[self.curr_option][1]()

    def switch(self, step: int) -> None:
        self.curr_option = (self.curr_option + step) % len(self.options)

    def draw(self, surf, x: int, y: int, spacing: int) -> None:
        for i, (text, _) in enumerate(self.options):
            color = (255, 255, 255) if i == self.curr_option else (100, 100, 100)
            surf.blit(self.font.render(text, True, color), (x, y + i * spacing))
