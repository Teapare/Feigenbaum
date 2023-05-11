import pygame

from constants import GRAPH_COLOR, BLACK


class TextField:
    def __init__(self, surf, pos, size, limit):
        self.surface = surf
        self.active = False
        self.limit = limit
        self.text = ""
        self.enter = None
        self.pos = pos
        self.size = size
        self.timer = 0
        self.caret_visible = False
        self.caret_pos = 0
        self.letter_space = 11
        self.maxlen = 12
        self.font = pygame.font.SysFont("Arial", 25)
        self.picture = None

    def connect(self, func):
        self.enter = func

    def redraw(self):
        if not self.text:
            self.picture = pygame.Surface((0, 0))
            return
        picture = self.font.render(self.text, True, BLACK)
        scale = picture.get_height() / (self.size[1] - 8)
        self.picture = picture
        # self.picture = pygame.transform.scale(picture, (picture.get_width() / scale, picture.get_height() / scale))

    def unfocus(self):
        if not(self.limit[0] <= float(self.text or 0) <= self.limit[1]):
            self.text = ""
            self.redraw()


    def draw(self):
        pygame.draw.rect(self.surface, GRAPH_COLOR, (self.pos, self.size))
        pygame.draw.rect(self.surface, BLACK, (self.pos, self.size), 2)
        if self.caret_visible:
            x = self.pos[0] + 10 + self.caret_pos * self.letter_space
            x = self.pos[0] + 10 + self.font.render(self.text[0:self.caret_pos], True, BLACK).get_width()
            pygame.draw.line(self.surface, BLACK, (x, self.pos[1] + 5), (x, self.pos[1] + self.size[1] - 5), 2)
        if self.picture:
            self.surface.blit(self.picture, (self.pos[0] + 10, self.pos[1]))
            # self.surface.blit(self.picture, (self.pos[0] + 10, self.pos[1] + 4))

    def get_click(self, pos):
        if self.pos[0] <= pos[0] <= self.pos[0] + self.size[0] and self.pos[1] <= pos[1] <= self.pos[1] + self.size[1]:
            return True
        return False

    def set_limit(self, limit):
        self.limit = limit

    def update(self, t):
        if self.active:
            self.timer += t
            if self.timer >= 500:
                self.timer -= 500
                self.caret_visible = not self.caret_visible

    def type(self, text):
        if self.maxlen == len(self.text):
            return
        if text == ".":
            if self.text.count(text) == 0:
                if self.caret_pos == 0:
                    self.text = "0." + self.text
                    self.move_caret(2)
                    self.redraw()
                    return
                self.text = self.text[0:self.caret_pos] + '.' + self.text[self.caret_pos:]
        else:
            self.text = self.text[0:self.caret_pos] + text + self.text[self.caret_pos:]
        self.move_caret(1)
        self.redraw()

    def erase(self, amount):
        if self.caret_pos < amount:
            return
        self.text = self.text[0: self.caret_pos - amount] + self.text[self.caret_pos:]
        self.caret_pos -= amount
        self.redraw()

    def move_caret(self, direction):
        self.caret_pos = max(0, min(len(self.text), self.caret_pos + direction))

    def key_press(self, key):
        if key == pygame.K_PERIOD:
            self.type(".")
        elif key == pygame.K_BACKSPACE:
            self.erase(1)
        elif key == pygame.K_RIGHT:
            self.move_caret(1)
        elif key == pygame.K_LEFT:
            self.move_caret(-1)
        else:
            self.type(str(key - 48))