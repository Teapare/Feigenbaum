import pygame

from constants import BLACK, GRAPH_COLOR
from textfield import TextField


class Button:
    def __init__(self, surf, pos, size, text, func):
        self.surface = surf
        self.pos = pos
        self.size = size
        self.image = pygame.transform.scale(pygame.font.SysFont("Arial", 25).render(text, True, BLACK),
                                            (self.size[0] - 10, self.size[1] - 10))
        self.function = func

    def draw(self):
        pygame.draw.rect(self.surface, GRAPH_COLOR, (self.pos, self.size))
        pygame.draw.rect(self.surface, BLACK, (self.pos, self.size), 2)
        self.surface.blit(self.image, (self.pos[0] + 5, self.pos[1] + 5))

    def get_click(self, pos):
        if self.pos[0] <= pos[0] <= self.pos[0] + self.size[0] and self.pos[1] <= pos[1] <= self.pos[1] + self.size[1]:
            print("BBBBB")
            self.function()
            return True
        return False


class SettingsWindow:
    def __init__(self, surf, pos, size):
        self.z = 0.4
        self.surface = surf
        self.pos = pos
        self.size = size
        self.minx = TextField(surf, (pos[0] + 20, pos[1] + 10), (150, 30), (0, 4), "min x")
        self.maxx = TextField(surf, (pos[0] + 20, pos[1] + 50), (150, 30), (float(self.minx.text or 0), 4), "max x")
        self.miny = TextField(surf, (pos[0] + 20, pos[1] + 90), (150, 30), (0, 1), "min y")
        self.maxy = TextField(surf, (pos[0] + 20, pos[1] + 130), (150, 30), (0, 1), "max y")
        self.draw_btn = Button(surf, (pos[0] + 20, pos[1] + 170), (60, 30), "Draw",
                               lambda: pygame.event.post(pygame.event.Event(pygame.USEREVENT)))
        self.fields = self.minx, self.maxx, self.miny, self.maxy

    def update(self, t):
        for field in self.fields:
            field.update(t)
        self.maxy.set_limit((float(self.miny.text or 0), 1))
        self.maxx.set_limit((float(self.minx.text or 0), 4))

    def draw(self):
        pygame.draw.rect(self.surface, BLACK, (self.pos, self.size), 2)
        for field in self.fields:
            field.draw()
        self.draw_btn.draw()

    def get_active(self, pos):
        if any(map(lambda field: field.get_click(pos), self.fields)):
            if pygame.mouse.get_cursor() != pygame.Cursor(pygame.SYSTEM_CURSOR_IBEAM):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_IBEAM)
            return True
        if pygame.mouse.get_cursor() != pygame.Cursor(pygame.SYSTEM_CURSOR_ARROW):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        return False

    def set_all_inactive(self):
        for field in self.fields:
            field.active = False
            field.timer = 0
            field.caret_visible = False
            field.unfocus()

    def get_click(self, pos):
        self.set_all_inactive()
        for field in self.fields:
            if field.get_click(pos):
                field.active = True
                field.caret_visible = True
        self.draw_btn.get_click(pos)

    def key_press(self, key):
        if key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8,
                   pygame.K_9, pygame.K_0, pygame.K_PERIOD, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_BACKSPACE]:
            for field in self.fields:
                if field.active:
                    field.key_press(key)
        if key == pygame.K_DOWN:
            pass
        if key == pygame.K_UP:
            pass
