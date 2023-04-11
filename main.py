import math

import pygame

BG_COLOR = pygame.Color(255, 255, 255)
BLACK = pygame.Color(0, 0, 0)
WINDOW_SIZE = 1200, 850
graph_pos = WINDOW_SIZE[0] - 800, 0
graph_size = 700, 700

DELTA_SCALE = 0.05


class Ruler:
    def __init__(self, pos, size, width, font, fontsize, bg_color, text_color):
        self.pos = pos
        self.size = size
        self.width = width
        self.font = pygame.font.SysFont(font, fontsize)
        self.bg_color = bg_color
        self.text_color = text_color

    def draw(self, surf):
        pygame.draw.rect(surf, BLACK, pygame.rect.Rect(*self.pos, *self.size), width=1)
        pygame.draw.rect(surf, BLACK, pygame.rect.Rect(self.pos[0] - self.width, self.pos[1], self.width + self.size[0],
                                                       self.width + self.size[1]), width=1)
        pygame.draw.line(surf, BLACK, (self.pos[0] - self.width, self.pos[1] + self.size[1] + self.width),
                         (self.pos[0], self.pos[1] + self.size[1]))

        for i in range(10):
            pygame.draw.line(surf, BLACK, (self.pos[0] + self.size[0] / 10 * i, self.pos[1] + self.size[1]),
                             (self.pos[0] + self.size[0] / 10 * i, self.pos[1] + self.size[1] + self.width / 2))
            pass


def pop(x, z, e):
    resd = {z: 1}
    for n in range(1000):
        z = x * (1 - z) * z
        if n < 100:
            continue
        newresd = resd.copy()
        g = False
        for item in resd:
            if abs(item - z) < e:
                newresd[item] += 1
                g = True
                break

        if not g:
            newresd[z] = 1
        resd = newresd.copy()
    return [key for key in resd if resd[key] > 2]


def draw(pos, scale, surf: pygame.Surface):
    h = surf.get_height()
    for x in range(800):
        for y in pop((scale * x + pos[0]) / surf.get_size()[0] * 4, 0.2, 0.001 * scale):
            pygame.draw.circle(surf, BLACK, (x, (h * (1 - y) - pos[1]) / scale), 1, 1)


def change_pos(pos, scale, rel):
    x, y = pos
    x = max(0, min(x - rel[0], 800 * (1 - scale)))
    y = max(0, min(y - rel[1], 800 * (1 - scale)))
    return x, y


def get_click(pos, size, click_pos):
    if click_pos[0] < pos[0]:
        return False
    if click_pos[0] > pos[0] + size[0]:
        return False
    if click_pos[1] > pos[1] + size[1]:
        return False
    if click_pos[1] < pos[1]:
        return False
    return True

def main():
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    graph = pygame.Surface(graph_size)

    ruler = Ruler((400, 0), graph_size, 50, "Arial", 24, BG_COLOR, BLACK)
    running = True
    scale = 1
    zoom = 1
    pos = (0, 0)
    redraw = True
    redraw_timer = 0
    drag = False
    fps = 30
    graph.fill(BG_COLOR)
    draw(pos, scale, graph)
    preview = pygame.transform.scale(graph, (200, 200))
    t = pygame.time.Clock()
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(scale, zoom, pos)
                if event.button == 1:
                    if get_click(graph_pos, graph_size, event.pos):
                        drag = True
                        pygame.mouse.get_rel()
                    elif get_click((4, 4), (200, 200), event.pos):
                        pass
                if event.button == 4 and zoom < 10:
                    zoom += 1
                    scale = 1 - math.log(zoom, 11)
                    vect = -DELTA_SCALE * 400, -DELTA_SCALE * 300
                    pos = change_pos(pos, scale, vect)
                    redraw = True
                    redraw_timer = 0
                if event.button == 5 and zoom > 1:
                    zoom -= 1
                    scale = 1 - math.log(zoom, 11)
                    vect = DELTA_SCALE * 400, DELTA_SCALE * 300
                    pos = change_pos(pos, scale, vect)
                    redraw = True
                    redraw_timer = 0
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                drag = False
        redraw_timer += t.tick(fps)
        screen.fill("White")
        if drag:
            pos = change_pos(pos, scale, pygame.mouse.get_rel())
            redraw = True
            redraw_timer = 0
        if redraw and redraw_timer > 20:
            graph.fill(BG_COLOR)
            draw(pos, scale, graph)
            redraw = False
        screen.blit(graph, graph_pos)
        screen.blit(preview, (4, 4))
        pygame.draw.rect(screen, BLACK, (0, 0, 208, 208), width=4)
        pygame.draw.rect(screen, pygame.Color("Red"),
                         (4 + pos[0] // 4, 4 + pos[1] // 4, int(scale * 200), int(scale * 200)),
                         width=1)
        # pygame.draw.line(screen, BLACK, (400, 0), (400, 800), 2)
        # pygame.draw.line(screen, BLACK, (400, 800), (1200, 800), 2)
        ruler.draw(screen)
        pygame.display.flip()


if __name__ == '__main__':
    main()
