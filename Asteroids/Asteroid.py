import random
import pygame
import math


class Asteroid:

    def __init__(self, vardict, colour, dir=None, speed=None):
        self.screen = vardict['screen']
        self.x = vardict['spawnx']
        self.y = vardict['spawny']
        self.costumes = vardict['costumes']
        self.scr_w = vardict['scr_w']
        self.scr_h = vardict['scr_h']
        if dir is None:
            self.dir = random.randint(0, 359)
        else:
            self.dir = dir
        if speed is None:
            self.speed = 1  # random.randint(1, 3)
        else:
            self.speed = speed
        # self.speed = speed
        self.costume_int = random.randint(vardict['aster_convert'] * 3 - 3, vardict['aster_convert'] * 3 - 1)
        self.costume = vardict['costumes'][self.costume_int]
        self.colrect = pygame.Rect((self.x, self.y), (self.costume.get_width(), self.costume.get_height()))
        self.score = 0
        self.colour = colour

    def move(self):
        self.colrect = pygame.Rect((self.x, self.y), (self.costume.get_width(), self.costume.get_height()))
        self.x += math.sin(math.radians(self.dir)) * self.speed
        self.y += math.cos(math.radians(self.dir)) * self.speed

    def draw(self):
        # print(f'coltopright: {self.colrect.topright}')
        # self.screen.blit(self.costume, (self.x, self.y))
        # hash below line to remove rectangles around the asteroids
        pygame.draw.rect(self.screen, self.colour, self.colrect, 1)

    def off_screen(self):
        if self.x - self.costume.get_width() > self.scr_w:
            self.x = 0 - self.costume.get_width()
        if self.x + self.costume.get_width() < 0:
            self.x = self.scr_w
        if self.y - self.costume.get_height() > self.scr_h:
            self.y = 0 - self.costume.get_height()
        if self.y + self.costume.get_height() < 0:
            self.y = self.scr_h

    def touching(self, shots, j):
        return self.colrect.collidepoint((shots[j].x, shots[j].y))

