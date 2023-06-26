import pygame

from constants import BG_COLOR, GRAPH_COLOR, BLACK, RED


class Graph:
    def __init__(self, parent: pygame.Surface, pos: tuple[float, float], size: tuple[float, float],
                 border_width: int):
        self.parent = parent
        self.pos = pos
        self.pos_nb = pos[0] + border_width, pos[1] + border_width
        self.size = size
        self.size_nb = size[0] - border_width * 2, size[1] - border_width * 2
        self.surface = pygame.Surface(self.size_nb)
        self.b_width = border_width
        self.redraw = False
        self.redraw_surf((0, 0, 4, 1), 0.4)
        self.scale = None
        self.selected = (0, 0)
        self.font = pygame.font.SysFont("Arial", 23)

    def update(self, rect, z, steps=1000):
        if self.redraw:
            self.redraw = False
            self.redraw_surf(rect, z, steps)

    def redraw_surf(self, rect, z, steps=1000):
        self.surface.fill(BG_COLOR)
        scale = max(rect[2] / 4, rect[3])
        r = pygame.Rect(0, 0, rect[2] / 4 / scale * self.size_nb[0], rect[3] / scale * self.size_nb[1])
        r.center = self.size_nb[0] / 2, self.size_nb[1] / 2
        pygame.draw.rect(self.surface, GRAPH_COLOR, r)
        for x in range(r.x, r.x + r.w):
            x_value = rect[0] + rect[2] / r.width * (x - r.x)
            for y_value in func(z, x_value, (rect[1], rect[3]), 0.001 * scale ** 2, steps):
                y = r.bottomright[1] - (y_value - rect[1]) / rect[3] * r.h
                pygame.draw.circle(self.surface, BLACK, (x, y), 1)
        self.scale = scale

    def get_in_area(self, pos):
        if self.pos_nb[0] < pos[0] < self.pos_nb[0] + self.size_nb[0] and self.pos_nb[1] < pos[1] < self.pos_nb[1] + \
                self.size_nb[1]:
            self.selected = pos[0] - self.pos_nb[0], pos[1] - self.pos_nb[1]
        else:
            self.selected = (0, 0)

    def draw(self, rect, ruler):
        pygame.draw.rect(self.parent, BLACK, (self.pos, self.size), width=self.b_width)
        self.parent.blit(self.surface, self.pos_nb)
        if self.selected[0]:
            pygame.draw.line(self.parent, RED, (self.pos_nb[0] + self.selected[0], self.pos_nb[1]),
                             (self.pos_nb[0] + self.selected[0], self.pos_nb[1] + self.size_nb[1]))
            text = self.font.render(f"{ruler.xrange[0] + (ruler.xrange[1] - ruler.xrange[0]) * self.selected[0] / self.size_nb[0]:.2f}", True, RED)
            self.parent.blit(text, (
                self.pos_nb[0] + self.selected[0] - text.get_width() * 0.5,
                self.pos[1] + self.size[1] + ruler.width * 0.5))
            self.parent.blit(text, (
                self.pos_nb[0] + self.selected[0] - text.get_width() * 0.5,
                self.pos[1] - ruler.width * 0.5 - text.get_height()))
            distance = 0
            while distance < self.size_nb[1]:
                if self.selected[1] + distance < self.size_nb[1] and self.surface.get_at(
                        (self.selected[0], self.selected[1] + distance)) == BLACK:
                    pygame.draw.circle(self.parent, RED, (
                        self.pos_nb[0] + self.selected[0], self.pos_nb[1] + self.selected[1] + distance), 5)
                    self.parent.blit(
                        self.font.render(
                            f"{rect[1] + rect[3] * (self.size_nb[1] - self.selected[1] - distance) / self.size_nb[1]:.2f}",
                            True, RED),
                        (self.pos_nb[0] + self.selected[0] + 10, self.pos_nb[1] + self.selected[1] + distance - 10))
                    break
                elif self.selected[1] - distance >= 0 and self.surface.get_at(
                        (self.selected[0], self.selected[1] - distance)) == BLACK:
                    pygame.draw.circle(self.parent, RED, (
                        self.pos_nb[0] + self.selected[0], self.pos_nb[1] + self.selected[1] - distance), 5)
                    self.parent.blit(
                        self.font.render(
                            f"{rect[1] + rect[3] * (self.size_nb[1] - self.selected[1] + distance) / self.size_nb[1]:.2f}",
                            True, RED),
                        (self.pos_nb[0] + self.selected[0] + 10, self.pos_nb[1] + self.selected[1] - distance - 10))
                    break
                distance += 1


def func(z, x, y_range: tuple[float, float], e, steps=1000):
    steps = max(steps, 1000)
    values = {}
    length = len(values)
    for n in range(steps):
        z = x * (1 - z) * z
        if n < 100:
            continue
        if n >= 300 and len(values) - length == 0:
            return values
        if z < y_range[0] or z > y_range[0] + y_range[1]:
            continue

        found_in_dict = False
        for item in list(values):
            if abs(item - z) < e:
                values[item] += 1
                found_in_dict = True
        if not found_in_dict:
            values[z] = 1
    return [float(key) for key in values if values[key] > 2]
