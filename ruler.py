import pygame

from constants import BLACK, BG_COLOR


class Ruler:
    def __init__(self, parent, pos, size, width):
        self.parent = parent
        self.pos = pos
        self.size = size
        self.width = width
        self.xrange = (0, 4)
        self.yrange = (0, 1)
        self.font = pygame.font.SysFont("Arial", 23)
        self.surf = pygame.Surface((size[0] + 2 * width, size[1] + 2 * width))
        self.redraw_surface()

    def redraw_surface(self):
        self.surf.fill(BG_COLOR)
        pygame.draw.rect(self.surf, BLACK, ((self.width, self.width), self.size), 2)
        pygame.draw.rect(self.surf, BLACK, (0, 0, self.size[0] + self.width * 2, self.size[1] + self.width * 2), 2)
        pygame.draw.line(self.surf, BLACK, (self.width, self.size[1] + self.width), (0, 2 * self.width + self.size[1]),
                         2)
        pygame.draw.line(self.surf, BLACK, (self.width, self.width), (0, 0), 2)
        pygame.draw.line(self.surf, BLACK, (self.width + self.size[0], self.width + self.size[1]),
                         (self.width * 2 + self.size[0], self.width * 2 + self.size[1]), 2)
        pygame.draw.line(self.surf, BLACK, (self.width + self.size[0], self.width), (self.width * 2 + self.size[0], 0),
                         2)
        for i in range(11):
            offset = i / 10
            pygame.draw.line(self.surf, BLACK, (self.width + self.size[0] * offset, self.width + self.size[1]),
                             (self.width + self.size[0] * offset, self.width * 1.5 + self.size[1]), 2)
            pygame.draw.line(self.surf, BLACK, (self.width + self.size[0] * offset, self.width),
                             (self.width + self.size[0] * offset, self.width * 0.5), 2)
            pygame.draw.line(self.surf, BLACK, (self.width, self.width + self.size[1] * offset),
                             (self.width * 0.5, self.width + self.size[1] * offset), 2)
            pygame.draw.line(self.surf, BLACK, (self.width + self.size[0], self.width + self.size[1] * offset),
                             (self.width * 1.5 + self.size[0], self.width + self.size[1] * offset), 2)
            if i == 10:
                break
            for k in range(10):
                offset = i / 10 + k / 100
                pygame.draw.line(self.surf, BLACK, (self.width + self.size[0] * offset, self.width + self.size[1]),
                                 (self.width + self.size[0] * offset, self.width * 1.125 + self.size[1]))
                pygame.draw.line(self.surf, BLACK, (self.width + self.size[0] * offset, self.width),
                                 (self.width + self.size[0] * offset, self.width * 0.875))
                pygame.draw.line(self.surf, BLACK, (self.width, self.width + self.size[1] * offset),
                                 (self.width * 0.875, self.width + self.size[1] * offset))
                pygame.draw.line(self.surf, BLACK, (self.width + self.size[0], self.width + self.size[1] * offset),
                                 (self.width * 1.125 + self.size[0], self.width + self.size[1] * offset))

    def update(self, newrangex, newrangey):
        if self.xrange == newrangex and newrangey == self.yrange:
            return
        self.xrange = newrangex
        self.yrange = newrangey

    def draw(self):
        self.parent.blit(self.surf, (self.pos[0] - self.width, self.pos[1] - self.width))
        text = self.font.render(f"{self.xrange[0]:.2f}", True, BLACK)
        self.parent.blit(text,
                         (self.pos[0] - text.get_width() / 2, self.pos[1] + self.size[1] + self.width / 2))
        self.parent.blit(text, (self.pos[0] - text.get_width() / 2, self.pos[1] - self.width / 2 - text.get_height()))
        text = self.font.render(f"{self.xrange[1]:.2f}", True, BLACK)
        self.parent.blit(text, (
            self.pos[0] + self.size[0] - text.get_width() / 2, self.pos[1] + self.size[1] + self.width / 2))
        self.parent.blit(text, (
            self.pos[0] + self.size[0] - text.get_width() / 2, self.pos[1] - self.width / 2 - text.get_height()))
        text = self.font.render(f"{self.yrange[0]:.2f}", True, BLACK)
        self.parent.blit(text, (self.pos[0] - text.get_width() - self.width / 2,
                                self.pos[1] + self.size[1] - text.get_height() / 2))
        self.parent.blit(text, (self.pos[0] + self.size[0] + self.width / 2,
                                self.pos[1] + self.size[1] - text.get_height() / 2))
        text = self.font.render(f"{self.yrange[1]:.2f}", True, BLACK)
        self.parent.blit(text, (
            self.pos[0] - text.get_width() - self.width / 2, self.pos[1] - text.get_height() / 2))
        self.parent.blit(text, (self.pos[0] + self.size[0] + self.width / 2, self.pos[1] - text.get_height() / 2))

        # for i in range(1, 11):
        #     offset = i / 10
        #     text = self.font.render(f"{(self.xrange[1] - self.xrange[0]) * offset:e}", True, BLACK)
        #     self.parent.blit(text, (self.pos[0] + offset * self.size[0] - text.get_width() * 0.5,
        #                             self.pos[1] + self.size[1] + self.width * 0.5))
        #     self.parent.blit(text, (self.pos[0] + offset * self.size[0] - text.get_width() * 0.5,
        #                             self.pos[1] - text.get_height() - self.width * 0.5))
        #     text = self.font.render(f"{(self.yrange[1] - self.yrange[0]) * offset}", True, BLACK)
        #     self.parent.blit(text, (self.pos[0] - self.width * 0.5 - text.get_width(),
        #                             self.pos[1] + offset * self.size[1] - text.get_height() * 0.5))
        #     self.parent.blit(text, (self.pos[0] + self.size[0] + self.width * 0.5,
        #                             self.pos[1] + offset * self.size[1] - text.get_height() * 0.5))
