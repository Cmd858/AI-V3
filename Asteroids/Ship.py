import random
import math

import pygame.draw
from pygame.locals import *

from Asteroid import *
from Shot import *


class Ship:
    def __init__(self, screen, net):
        """Init function for ship class, screen arg as reference to pygame display screen"""
        self.screen = screen
        self.net = net
        self.runNet = net.runNet
        self.scrW = screen.get_width()
        self.scrH = screen.get_height()
        self.x = 300
        self.y = 300
        self.dx = 0
        self.dy = 0
        self.dir = 0
        self.hyp = 0.1  # hypotenuse of movement
        self.costume = pygame.image.load('Images/ship_fly.png').convert()
        self.colrect = self.costume.get_rect()
        self.width = self.costume.get_width()
        self.height = self.costume.get_height()
        self.costume.set_colorkey((0, 0, 0))
        self.shots = []
        self.asteroids: list[Asteroid] = []
        self.lastShot = 0
        self.shotdelay = 30
        self.asteroidcount = 5
        self.makeAsteroids()
        self.dead = False
        self.asteroidScores = [100, 50, 20]
        self.score = 0
        self.outputList = [0, 0, 0, 0]
        self.inputList = []
        # self.outputList = [random.randint(0, 1) for _ in range(4)]

    def reset(self):
        # print(self.score)
        self.score = 0
        self.x = 300
        self.y = 300
        self.dx = 0
        self.dy = 0
        self.dir = 0
        self.dead = False
        self.asteroids = []
        self.shots = []
        self.makeAsteroids()
        self.lastShot = 0

    def draw(self):
        """Draw the ship to the screen"""
        rotated = pygame.transform.rotate(self.costume, self.dir)
        self.screen.blit(rotated,
                         (self.x - rotated.get_width() / 2,
                          self.y - rotated.get_height() / 2))
        pygame.draw.rect(self.screen, (255, 255, 255), self.colrect, 1)

    def move(self, drawrays):
        """Move ship based on outputList"""
        self.inputList = self.raycast(drawrays)
        self.net.runNet(self.inputList)
        self.outputList = self.net.getOut()  # def not how outputList should be used
        # print(self.outputList)
        if self.outputList[0] > 0.5:
            self.dir -= 4
        if self.outputList[1] > 0.5:
            self.dir += 4
        self.dir = self.dir % 360
        if self.outputList[2] > 0.5:
            self.dx -= self.hyp * math.sin(math.radians(self.dir))
            self.dy -= self.hyp * math.cos(math.radians(self.dir))
        if self.outputList[3] > 0.5:
            if self.lastShot >= self.shotdelay:
                self.shots.append(Shot(self.screen, self.x, self.y, self.dir))
                self.lastShot = 0
        self.x = (self.x + self.dx) % self.scrW
        self.y = (self.y + self.dy) % self.scrH
        self.dx *= 0.99
        self.dy *= 0.99
        self.colrect.x = self.x - self.width / 2
        self.colrect.y = self.y - self.height / 2
        self.lastShot += 1

    def controlMove(self):
        self.inputList = self.raycast()
        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            self.dir -= 4
        if keys[K_RIGHT]:
            self.dir += 4
        self.dir = self.dir % 360
        if keys[K_UP]:
            self.dx -= self.hyp * math.sin(math.radians(self.dir))
            self.dy -= self.hyp * math.cos(math.radians(self.dir))
        if keys[K_SPACE]:
            if self.lastShot >= self.shotdelay:
                self.shots.append(Shot(self.screen, self.x, self.y, self.dir))
                self.lastShot = 0
        self.x = (self.x + self.dx) % self.scrW
        self.y = (self.y + self.dy) % self.scrH
        self.dx *= 0.99
        self.dy *= 0.99
        self.colrect.x = self.x - self.width / 2
        self.colrect.y = self.y - self.height / 2
        self.lastShot += 1

    def processShots(self):
        i = 0
        while i < len(self.shots):
            shot = self.shots[i]
            shot.move()
            shot.draw()
            shot.tick()
            if shot.despawnable():
                self.shots.pop(i)
                i -= 1
            i += 1

    def makeAsteroids(self):
        #positions = [(0, 0, 0)]
        positions = [(0, 0, i/self.asteroidcount*360 + -10) for i in range(self.asteroidcount)]
        for position in positions:
            self.asteroids.append(Asteroid(self.screen, *position, 1, 2))

    def processAsteroids(self):
        i = 0
        shotPoints = [(shot.x, shot.y) for shot in self.shots]  # get positions of all shots
        while i < len(self.asteroids):
            self.asteroids[i].move()
            collision, size = self.asteroids[i].hasBeenShot(shotPoints)
            if collision is not None:
                self.score += self.asteroidScores[size]
                if size != 0:
                    self.asteroids.append(Asteroid(self.screen, self.asteroids[i].x, self.asteroids[i].y,
                                                   self.asteroids[i].dir + 10, self.asteroids[i].hyp + 0.25, size - 1))
                    self.asteroids.append(Asteroid(self.screen, self.asteroids[i].x, self.asteroids[i].y,
                                                   self.asteroids[i].dir - 10, 1, size - 1))
                del self.asteroids[i]
                del self.shots[collision]
                shotPoints = [(shot.x, shot.y) for shot in self.shots]  # recalculate to prevent double deletion
                continue  # skip draw as current has been deleted
            if self.asteroids[i].rect.colliderect(self.colrect):
                self.dead = True  # been hit by asteroid so must be dead
            self.asteroids[i].draw()
            i += 1
        if len(self.asteroids) == 0:
            self.makeAsteroids()

    def raycast(self, drawrays):
        """Emit rays that can be used to detect asteroids"""
        rays = 8
        raylen = 500
        centreX = self.x  # + self.width / 2
        centreY = self.y  # + self.height / 2
        colour = [80, 80, 80]
        collided = []
        for i in range(int(rays/2)):
            rayrad = math.radians(360/rays*i - self.dir)  # self.dir at end bc maths goes anticlockwise but not sprites
            lineEnd = (centreX + raylen * math.cos((rayrad)),
                       centreY + raylen * math.sin((rayrad)))
            for asteroid in self.asteroids:
                clipTup = asteroid.rect.clipline(centreX, centreY, *lineEnd)
                if len(clipTup) != 0:
                    lineEnd = clipTup[0]
            if drawrays:
                pygame.draw.line(self.screen, colour, (centreX, centreY), lineEnd, 2)
            collided.append(math.dist((centreX, centreY), lineEnd))
            for j in range(len(colour)):
                colour[j] += 20
        for i in range(int(rays/2)):
            rayrad = math.radians(360 / rays * i - self.dir)
            lineEnd = (centreX - raylen * math.cos((rayrad)),
                       centreY - raylen * math.sin((rayrad)))
            for asteroid in self.asteroids:
                clipTup = asteroid.rect.clipline(centreX, centreY, *lineEnd)
                if len(clipTup) != 0:
                    lineEnd = clipTup[0]
            if drawrays:
                pygame.draw.line(self.screen, colour, (centreX, centreY), lineEnd, 2)
            collided.append(math.dist((centreX, centreY), lineEnd))
            for j in range(len(colour)):
                colour[j] += 20
        for i, dist in enumerate(collided):
            collided[i] = 1/dist*raylen
        return collided
