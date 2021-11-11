import math
import pygame
import time


class Shot:

    def __init__(self, vardict, ship, colour=(255,255,255)):
        self.vardict = vardict
        self.x = ship.x + ship.costume.get_width() / 2
        self.y = ship.y + ship.costume.get_height() / 2
        self.dx = -math.sin(math.radians(ship.dir)) * 5
        self.dy = -math.cos(math.radians(ship.dir)) * 5
        self.deathtick = 0
        self.screen = vardict['screen']
        self.colour = colour

    def move(self):
        self.x += self.dx
        self.y += self.dy
        self.deathtick += 1

    def draw(self):
        pygame.draw.circle(self.screen, self.colour, (int(self.x), int(self.y)), 1)

    def off_screen(self):
        if self.x > self.vardict['scr_w']:
            self.x = 0
        if self.x < 0:
            self.x = self.vardict['scr_w']
        if self.y > self.vardict['scr_h']:
            self.y = 0
        if self.y < 0:
            self.y = self.vardict['scr_h']

    def delete(self):
        return self.deathtick > 120
