import pygame
from constants import *
from settings import SettingsWindow
from graph import Graph
from previewer import Previewer
from ruler import Ruler


class App:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(WINDOW_SIZE)
        self.graph = Graph(self.screen, (400, 10), (606, 606), 3)
        self.previewer = Previewer(self.screen, (10, 10), (208, 208), 4, self.graph.surface)
        self.ruler = Ruler(self.screen, (400, 10), (606, 606), 75)
        self.settings = SettingsWindow(self.screen, (50, 250), (200, 300))

        self.steps = 1000
        self.graph.redraw = True
        self.fps = FPS
        self.running = False
        self.timer = pygame.time.Clock()

    def handle_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.previewer.get_click(event.pos):
                        self.previewer.start_drag()
                    self.settings.get_click(event.pos)

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if self.previewer.drag:
                        self.previewer.finish_drag()
                        self.graph.redraw = True
            if event.type == pygame.MOUSEMOTION:
                self.settings.get_active(event.pos)

            if event.type == pygame.KEYDOWN:
                self.settings.key_press(event.key)

            if event.type == pygame.USEREVENT:
                self.custom_graph_redraw()

    def custom_graph_redraw(self):
        if any(map(lambda field: field.text == "", self.settings.fields)):
            return
        x, y, w, h = float(self.settings.minx.text), float(self.settings.miny.text), float(
            self.settings.maxx.text), float(self.settings.maxy.text)
        w, h = w - x, h - y
        self.graph.redraw_surf((x, y, w, h), self.settings.z, self.steps)
        # TODO: change previewer selected rectangle as well.

    def update(self):
        t = self.timer.tick(self.fps)
        self.previewer.update()
        self.graph.update(self.previewer.get_selected(), self.settings.z, self.steps)
        self.settings.update(t)

    def draw(self):
        self.screen.fill(BG_COLOR)
        self.previewer.draw()
        self.graph.draw()
        # self.ruler.draw()
        self.settings.draw()

        pygame.display.flip()

    def run(self):
        self.running = True
        while self.running:
            self.update()
            self.handle_events()
            self.draw()


if __name__ == '__main__':
    app = App()
    app.run()
