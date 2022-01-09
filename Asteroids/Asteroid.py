import pygame
import math


class Asteroid:
    def __init__(self, screen, x, y, dir, hyp, size):
        self.screen = screen
        self.x = x
        self.y = y
        self.size = size
        self.sizes = (25, 50, 100)
        self.length = self.sizes[self.size]
        self.rect = pygame.Rect(self.x, self.y, self.length, self.length)
        self.dir = dir
        self.hyp = hyp
        self.dx = self.hyp * math.sin(math.radians(self.dir))
        self.dy = self.hyp * math.cos(math.radians(self.dir))
        self.scrW = screen.get_width()
        self.scrH = screen.get_height()

    def draw(self):
        pygame.draw.rect(self.screen, (255, 255, 255), self.rect, 1)

    def move(self):
        self.x = (self.x - self.dx + self.length) % (self.scrW + self.length) - self.length
        self.y = (self.y - self.dy + self.length) % (self.scrH + self.length) - self.length
        self.rect.x, self.rect.y = self.x, self.y

    def hasBeenShot(self, points):
        for i, point in enumerate(points):
            if self.rect.collidepoint(point):
                return i, self.size
        return None, self.size
