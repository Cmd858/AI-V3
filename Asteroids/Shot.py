import math
import pygame


class Shot:
    def __init__(self, screen, x, y, dir):
        self.screen = screen
        self.x = x
        self.y = y
        self.dir = dir
        self.hyp = 8
        self.scrW = screen.get_width()
        self.scrH = screen.get_height()
        self.dx = self.hyp * math.sin(math.radians(self.dir))
        self.dy = self.hyp * math.cos(math.radians(self.dir))
        self.ticks = 0
        self.maxticksalive = 90

    def move(self):
        self.x = (self.x - self.dx) % self.scrW
        self.y = (self.y - self.dy) % self.scrH

    def draw(self):
        pygame.draw.circle(self.screen, (255, 255, 255), (self.x, self.y), 1)

    def tick(self):
        self.ticks += 1

    def despawnable(self):
        return self.ticks > self.maxticksalive