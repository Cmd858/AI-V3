from pygame.locals import *
from pygame.font import SysFont

from Asteroid import *
# from Net2 import Net
from Shot import *


# import copy


class Ship:

    def __init__(self, vardict, colour, netfunc):
        # netfunc is function reference for corresponding net class
        # net False means human controlled, otherwise None = random, net class = mutated
        if netfunc is False:
            self.netfunc = False
        elif netfunc is None:
            pass
            # self.netfunc = Net(8, 4, 0.05, 0.25, 0.5, 0.1, (-2, 0), 5)  # edit net values in population
            # self.netfunc.mutate()
        else:
            self.netfunc = netfunc  # function to get net output
        self.vardict = vardict
        self.x = vardict['scr_w'] / 2
        self.y = vardict['scr_h'] / 2
        self.scr_w = vardict['scr_w']
        self.scr_h = vardict['scr_h']
        self.screen = vardict['screen']
        self.dir = 0
        self.xmomentum = 0
        self.ymomentum = 0
        self.ship_still = vardict['ship_still']
        self.ship_move = vardict['ship_move']
        self.costume = self.ship_still
        self.rotated = pygame.transform.rotate(self.ship_move, self.dir)
        self.colrect = pygame.Rect((self.x, self.y), (self.costume.get_width(), self.costume.get_height()))
        self.normwidth = self.costume.get_width()
        self.normheight = self.costume.get_height()
        self.invul = time.time() + 100000
        self.lives = 3
        self.asteroids = []
        self.shots = []
        self.score = 0
        self.movements = []  # output values from net if used
        self.colour = colour
        self.shotdelay = 0
        self.rays = []
        self.font2 = SysFont('lucidaconsole', 20)

    def take_values(self, vallist):
        self.movements = vallist

    def draw(self, drawrays=False):
        # print(self.score, self.lives)
        pygame.draw.rect(self.screen, self.colour, self.colrect, 1)
        if drawrays:
            for i in range(len(self.rays)):
                pygame.draw.line(self.screen, self.colour, self.rays[i][0], self.rays[i][1], 2)
        pressed_keys = pygame.key.get_pressed()
        if not (self.invul + 3 > time.time() and (int(time.time()) * 4 % 4 == 1 or int(time.time()) * 4 % 4 == 3)):
            if pressed_keys[K_UP]:
                self.rotated = pygame.transform.rotate(self.ship_move, self.dir)
                self.colrect = pygame.Rect((self.x, self.y), (self.normwidth, self.normheight))
                self.screen.blit(self.rotated,
                                 (self.x - 0.5 + self.ship_move.get_width() / 2 - self.rotated.get_width() / 2,
                                  self.y + self.ship_move.get_height() / 2 - self.rotated.get_height() / 2))
                self.costume = self.ship_move
            else:
                self.rotated = pygame.transform.rotate(self.ship_still, self.dir)
                self.colrect = pygame.Rect((self.x, self.y), (self.normwidth, self.normheight))
                self.screen.blit(self.rotated, (self.x +
                                                self.ship_still.get_width() / 2 - self.rotated.get_width() / 2,
                                                self.y +
                                                self.ship_still.get_height() / 2 - self.rotated.get_height() / 2))
                self.costume = self.ship_still

    def move(self, printins=False):
        self.shotdelay += 1
        if self.netfunc is False:
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[K_RIGHT]:
                self.dir -= 6
            if pressed_keys[K_LEFT]:
                self.dir += 6  # should rotate fully in 1 second instead of 1.5
            if pressed_keys[K_UP]:
                if self.xmomentum + self.ymomentum < 0.1 or self.xmomentum + self.ymomentum > -0.1:
                    self.xmomentum += math.sin(math.radians(self.dir)) * -0.1
                    self.ymomentum += math.cos(math.radians(self.dir)) * -0.1
            else:
                if self.xmomentum + self.ymomentum != 0:
                    if self.xmomentum > 0:
                        self.xmomentum -= 0.05
                    else:
                        self.xmomentum += 0.025
                    if self.ymomentum > 0:
                        self.ymomentum -= 0.05
                    else:
                        self.ymomentum += 0.025
            self.x += self.xmomentum
            self.y += self.ymomentum
        else:
            ins = self.raycast(0)
            if printins:
                txt = self.font2.render('Input Values:', True, (255, 255, 255))
                drop = txt.get_height() + 5
                self.screen.blit(txt, (0, drop * (9)))
                for i in range(len(ins)):
                    txt = self.font2.render(f'{ins[i]}', True, (255, 255, 255))
                    drop = txt.get_height() + 5
                    self.screen.blit(txt, (0, drop * (i + 10)))
            self.movements = self.netfunc(ins)  # == net.run_net() as function reference
            if self.movements[0] > 0:
                self.dir -= 4
            if self.movements[1] > 0:
                self.dir += 4
            if self.movements[2] > 0:
                if self.xmomentum + self.ymomentum < 0.1 or self.xmomentum + self.ymomentum > -0.1:
                    self.xmomentum += math.sin(math.radians(self.dir)) * -0.1
                    self.ymomentum += math.cos(math.radians(self.dir)) * -0.1
            else:
                if self.xmomentum + self.ymomentum != 0:
                    if self.xmomentum > 0:
                        self.xmomentum *= 0.95
                    else:
                        self.xmomentum += 0.025
                    if self.ymomentum > 0:
                        self.ymomentum *= 0.95
                    else:
                        self.ymomentum += 0.025
            if self.movements[3] > 0:
                self.shoot()
            self.x += self.xmomentum
            self.y += self.ymomentum
            while self.dir > 360:
                self.dir -= 360
            while self.dir < 0:
                self.dir += 360

    def off_screen(self):
        if self.x > self.scr_w:
            self.x = 0
        if self.x < 0:
            self.x = self.scr_w
        if self.y > self.scr_h:
            self.y = 0
        if self.y < 0:
            self.y = self.scr_h

    def life_lost(self):
        self.lives -= 1
        self.invul = time.time()

    def hit(self):
        for i in range(len(self.asteroids)):
            if self.colrect.colliderect(self.asteroids[i].colrect):
                return True
        return False

    def gametick(self, drawbool, fixedpattern=True):
        if len(self.asteroids) == 0:
            aster_convert = 1
            self.vardict['aster_convert'] = aster_convert
            #  if asteroid_spawn < time.time() - 2:
            for i in range(0, 5):
                self.vardict['spawnx'] = 0  # random.randint(0, self.scr_w)
                self.vardict['spawny'] = 0  # random.randint(0, self.scr_h)
                self.asteroids.append(
                    Asteroid(self.vardict, self.colour, i * 72 if fixedpattern else None))
                #  i*72  # used to test consistency
        i = 0
        while i < len(self.shots):
            if drawbool:
                self.shots[i].draw()
            self.shots[i].move()
            self.shots[i].off_screen()
            if self.shots[i].delete():
                del self.shots[i]
                i -= 1
            i += 1
        i = 0
        while i < len(self.asteroids):
            if drawbool:
                self.asteroids[i].draw()
            self.asteroids[i].move()
            self.asteroids[i].off_screen()
            j = 0
            while j < len(self.shots):
                if self.asteroids[i].touching(self.shots, j):
                    if self.asteroids[i].costume_int < 3:
                        self.vardict['aster_convert'] = 2
                        self.vardict['spawnx'] = self.asteroids[i].x
                        self.vardict['spawny'] = self.asteroids[i].y
                        self.asteroids.append(Asteroid(self.vardict, self.colour, self.asteroids[i].dir - 20))
                        self.asteroids.append(Asteroid(self.vardict, self.colour, self.asteroids[i].dir + 20))
                        del self.asteroids[i]
                        del self.shots[j]
                        self.score += 20
                        i -= 1
                        j -= 1
                        break
                    elif self.asteroids[i].costume_int < 6:
                        self.vardict['aster_convert'] = 3
                        self.vardict['spawnx'] = self.asteroids[i].x
                        self.vardict['spawny'] = self.asteroids[i].y
                        self.asteroids.append(Asteroid(self.vardict, self.colour, self.asteroids[i].dir - 20))
                        self.asteroids.append(Asteroid(self.vardict, self.colour, self.asteroids[i].dir + 20))
                        del self.asteroids[i]
                        del self.shots[j]
                        self.score += 50
                        i -= 1
                        j -= 1
                        break
                    else:
                        del self.asteroids[i]
                        del self.shots[j]
                        self.score += 100
                        i -= 1
                        j -= 1
                        break
                j += 1
            i += 1

    def shoot(self):
        if self.shotdelay >= 15:
            self.shots.append(Shot(self.vardict, self, self.colour))
            self.shotdelay = 0

    def collide(self, xy12, xy34):
        x1 = xy12[0][0]
        y1 = xy12[0][1]
        x2 = xy12[1][0]
        y2 = xy12[1][1]
        x3 = xy34[0][0]
        y3 = xy34[0][1]
        x4 = xy34[1][0]
        y4 = xy34[1][1]
        # print(y4, y3, x4, x3)
        g1 = (y2 - y1) / (x2 - x1) if x2 - x1 != 0 else 10000
        g2 = (y4 - y3) / (x4 - x3) if x4 - x3 != 0 else 10000

        c1 = y1 - g1 * x1
        c2 = y3 - g2 * x3

        x = (c1 - c2) / (g2 - g1) if g2 - g1 != 0 else 10000

        y = g1 * x + c1
        if (x1 <= x <= x2 or x1 >= x >= x2) and (x3 <= x <= x4 or x3 >= x >= x4) \
                and (y1 <= y <= y2 or y1 >= y >= y2) and (y3 <= y <= y4 or y3 >= y >= y4):
            return x, y
        else:
            return False

    def raycast(self, nocollisionval, raynum=8, raydist=1000):
        rays = []  # add ship rays to this # rays represented as ((x1, y1), (x2, y2))
        centre = self.colrect.center
        for i in range(int(raynum/2)):
            grad = math.tan((360 - self.dir + (i * (360 / raynum))) / (180 / math.pi))  # use this for grads of rays
            x2 = (centre[0]) + raydist  # rays can be any length
            dy2 = grad * x2  # delta y, aka change in y
            y2 = dy2 + centre[1]
            rays.append((centre, (x2, y2)))
        for i in range(int(raynum/2)):
            grad = math.tan((360 - self.dir + (i * (360 / raynum))) / (180 / math.pi))  # use this for grads of rays
            x2 = (centre[0]) - raydist  # rays can be any length
            dy2 = grad * x2  # delta y, aka change in y
            y2 = dy2 + centre[1]
            rays.append((centre, (x2, y2)))
        self.rays = rays
        rayvals = []
        for i in range(len(rays)):
            colval = False
            for j in range(len(self.asteroids)):
                rect = self.asteroids[j].colrect
                lines = ((rect.topright, rect.bottomright), (rect.bottomright, rect.bottomleft),
                         (rect.bottomleft, rect.topleft), (rect.topleft, rect.topright))
                for k in range(4):
                    val = self.collide(rays[i], lines[k])
                    if val is not False:
                        colval = True
                        break
                if colval:
                    break
            if colval:
                rayvals.append(val)  # unindenting this section to test fix
                continue
            else:
                rayvals.append(False)

        raydists = []
        for i in range(len(rayvals)):
            if rayvals[i] is not False:
                raydists.append((rayvals[i][0] ** 2 + rayvals[i][1] ** 2) ** 0.5)  # pythag
            else:
                raydists.append(nocollisionval if i < len(rayvals)/2 else -nocollisionval)
                # correct for missing bottom line that doesn't work :|
        return raydists

# TODO: Now there are 7 some of the time... yay
# TODO: correct downward ray overlapping upward due to ZeroDivisionError setting to positive number(maybe)
