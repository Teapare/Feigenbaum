import pygame

from constants import BLACK, RED, GREEN


class Previewer:
    def __init__(self, parent: pygame.Surface, pos: tuple[float, float], size: tuple[float, float], border_width,
                 image: pygame.Surface):
        self.parent = parent
        self.pos = pos
        self.pos_nb = pos[0] + border_width, pos[1] + border_width
        self.size = size
        self.border_width = border_width
        self.size_nb = size[0] - border_width * 2, size[1] - border_width * 2
        self.image = pygame.transform.scale(image, self.size_nb)
        self.selected_rect = pygame.rect.Rect(self.pos_nb, self.size_nb)
        self.drag = False
        self.drag_starting_pos = (0, 0)
        self.selector_rect = pygame.rect.Rect(0, 0, 0, 0)

    def update(self):
        if self.drag:
            x, y = pygame.mouse.get_pos()
            x, y = x - self.drag_starting_pos[0], y - self.drag_starting_pos[1]
            self.selector_rect.update(*self.drag_starting_pos, x, y)
            self.selector_rect.normalize()
            self.selector_rect = self.selector_rect.clip(self.pos_nb, self.size_nb)

    def finish_drag(self):
        self.drag = False
        if self.selector_rect.w == 0 and 0 == self.selector_rect.h:
            self.selected_rect.update(self.pos_nb, self.size_nb)
            return
        self.selected_rect = self.selector_rect.copy()
        self.selector_rect.update(0, 0, 0, 0)

    def start_drag(self):
        self.drag = True
        self.drag_starting_pos = pygame.mouse.get_pos()
        self.selector_rect.update(*self.drag_starting_pos, 0, 0)

    def get_selected(self):
        x = (self.selected_rect.x - self.pos_nb[0]) * 4 / self.size_nb[0]
        y = 1 - (self.selected_rect.y - self.pos_nb[1] + self.selected_rect.h) / self.size_nb[1]
        w = self.selected_rect.w / self.size_nb[0] * 4
        h = self.selected_rect.h / self.size_nb[1]
        return x, y, w, h

    def get_click(self, pos: tuple[float, float]):
        actual_pos = pos[0] - self.pos[0], pos[1] - self.pos[1]
        if not (self.border_width <= actual_pos[0] <= self.size[0] - self.border_width):
            return False
        if not (self.border_width <= actual_pos[1] <= self.size[1] - self.border_width):
            return False
        return True

    def select(self, x, y, w, h):
        self.selected_rect.update(x, y, w, h)

    def draw(self):
        pygame.draw.rect(self.parent, BLACK, (*self.pos, *self.size))
        self.parent.blit(self.image, (self.pos[0] + self.border_width, self.pos[1] + self.border_width))
        pygame.draw.rect(self.parent, RED, self.selected_rect, width=1)
        pygame.draw.rect(self.parent, GREEN, self.selector_rect, width=1)
