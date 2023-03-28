import math

import pygame

BG_COLOR = pygame.Color(255, 255, 255)
BLACK = pygame.Color(0, 0, 0)
WINDOW_SIZE = 900, 700
graph_pos = WINDOW_SIZE[0] - 800, 0

DELTA_SCALE = 0.05


def pop(x, z, e):
    resd = {z: 1}
    br = False
    for n in range(1000):
        z = x * (1 - z) * z
        newresd = resd.copy()
        g = False
        for item in resd:
            if newresd[item] > 2:
                br = True
                break
            if abs(item - z) < e:
                newresd[item] += 1
                g = True
                break

        if not g:
            newresd[z] = 1
        resd = newresd.copy()
        if br:
            break
    return [key for key in resd if resd[key] > 1]


def draw(pos, scale, surf: pygame.Surface):
    h = surf.get_height()
    for x in range(800):
        for y in pop((scale * x + pos[0]) / 200, 0.2, 0.001 * scale):
            # print(x, y)
            if pos[1] < (1 - y) * scale * h < pos[1] + h * scale:
                pygame.draw.circle(surf, BLACK, (x, scale * (1 - y) * h - pos[1]), 1, 1)


def change_pos(pos, scale, rel):
    x, y = pos
    x = max(0, min(x - rel[0], 800 * (1 - scale)))
    y = max(0, min(y - rel[1], 600 * (1 - scale)))
    return x, y


def main():
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    graph = pygame.Surface((800, 600))

    running = True
    scale = 1
    zoom = 1
    pos = (0, 0)
    redraw = True
    drag = False

    fps = 30
    t = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(scale, zoom, pos)
                if event.button == 1:
                    drag = True
                    pygame.mouse.get_rel()
                if event.button == 4 and zoom < 10:
                    zoom += 1
                    scale = 1 - math.log(zoom, 11)
                    vect = -DELTA_SCALE * 400, -DELTA_SCALE * 300
                    pos = change_pos(pos, scale, vect)
                    redraw = True
                if event.button == 5 and zoom > 1:
                    zoom -= 1
                    scale = 1 - math.log(zoom, 11)
                    vect = DELTA_SCALE * 400, DELTA_SCALE * 300
                    pos = change_pos(pos, scale, vect)
                    redraw = True
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                drag = False
        t.tick(fps)
        if drag:
            pos = change_pos(pos, scale, pygame.mouse.get_rel())
            redraw = True
        if redraw:
            graph.fill(BG_COLOR)
            draw(pos, scale, graph)
            redraw = False
        screen.blit(graph, graph_pos)
        pygame.display.flip()


if __name__ == '__main__':
    main()
