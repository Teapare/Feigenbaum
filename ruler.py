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
        for i in range(10):
            pygame.draw.line(self.parent, BLACK, (self.pos[0] + self.size[0] * i / 10, self.pos[1] + self.size[1]),
                             (self.pos[0] + self.size[0] * i / 10, self.pos[1] + self.size[1] + self.width / 2), 2)
            pygame.draw.line(self.parent, BLACK, (self.pos[0], self.pos[1] + self.size[1] * (i + 1) / 10),
                             (self.pos[0] - self.width / 2, self.pos[1] + self.size[1] * (i + 1) / 10), 2)
            for k in range(10):
                pygame.draw.line(self.parent, BLACK,
                                 (self.pos[0] + self.size[0] * (i / 10 + k / 100), self.pos[1] + self.size[1]),
                                 (self.pos[0] + self.size[0] * (i / 10 + k / 100),
                                  self.pos[1] + self.size[1] + self.width / 8))
                pygame.draw.line(self.parent, BLACK, (self.pos[0], self.pos[1] + self.size[1] * (i / 10 + k / 100)),
                                 (self.pos[0] - self.width / 8, self.pos[1] + self.size[1] * (i / 10 + k / 100)))
