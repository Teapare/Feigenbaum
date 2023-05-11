import pygame

from constants import BLACK


class Ruler:
    def __init__(self, parent, pos, size, width):
        self.parent = parent
        self.pos = pos
        self.size = size
        self.width = width
        self.xrange = (0, 4)

    def update(self, newrange):
        if self.xrange == newrange:
            return
        self.xrange = newrange

    def draw(self):
        pygame.draw.rect(self.parent, BLACK, (self.pos, self.size), 2)
        pygame.draw.rect(self.parent, BLACK,
                         (self.pos[0] - self.width, self.pos[1], self.size[0] + self.width, self.size[1] + self.width),
                         2)
        pygame.draw.line(self.parent, BLACK, (self.pos[0], self.pos[1] + self.size[1]),
                         (self.pos[0] - self.width, self.pos[1] + self.width + self.size[1]), 2)