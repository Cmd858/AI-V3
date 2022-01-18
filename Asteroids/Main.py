import random

import pygame
import sys
from pygame.locals import *

from Ship import Ship
from NEAT.Population import Pop


def controls():
    global drawRays
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit(0)
        if event.type == KEYDOWN and event.key == K_r:
            drawRays = not drawRays
        if event.type == KEYDOWN and event.key == K_g:
            population.plotGraph()


def ui(screen, ui_open):
    offset = 0
    if ui_open:
        screen.blit(font2.render(f'Gen: {population.gen}',
                                 True, (255, 255, 255), None), (0, offset * 20))
        offset += 1
        screen.blit(font2.render(f'FPS: {int(clock.get_fps())}',
                                 True, (255, 255, 255), None), (0, offset * 20))
        offset += 1
        screen.blit(font2.render(f'Ships: {shipcount - shipsDead}/{shipcount}',
                                 True, (255, 255, 255), None), (0, offset * 20))
        offset += 1
        screen.blit(font2.render(f'Highest score: {max([ship.score for ship in ships])}',
                                 True, (255, 255, 255), None), (0, offset * 20))
        offset += 1
        screen.blit(font2.render(f'HighScore: {lifeHighScore}',
                                 True, (255, 255, 255), None), (0, offset * 20))
        offset += 1
        screen.blit(font2.render(f'DrawRays: {drawRays}',
                                 True, (255, 255, 255), None), (0, offset * 20))
        offset += 1
        screen.blit(font2.render(f'Species: {len(population.species)}',
                                 True, (255, 255, 255), None), (0, offset * 20))
        offset += 1


if __name__ == '__main__':
    pygame.init()
    clock = pygame.time.Clock()
    pygame.display.set_caption("Asteroids")
    screen = pygame.display.set_mode((700, 600))
    scr_w = screen.get_width()
    scr_h = screen.get_height()
    font = pygame.font.SysFont('lucidaconsole', 60)
    font2 = pygame.font.SysFont('lucidaconsole', 20)
    ships: [Ship] = []
    shipcount = 200
    # shipcount = 50
    drawRays = False

    highestScore = 0
    lifeHighScore = 0

    # net config
    netNum = shipcount
    inNum = 8
    outNum = 4
    connectionMutationChance = 0.05
    nodeMutationChance = 0.03
    weightMutationChance = 0.8
    crossoverNum = 3

    population = Pop(netNum,
                     inNum,
                     outNum,
                     connectionMutationChance,
                     nodeMutationChance,
                     weightMutationChance,
                     crossoverNum)

    population.populate()
    for i in range(shipcount):
        ships.append(Ship(screen, population.population[i]))
    for _ in range(5):
        population.mutateNets((1, 2))
    while 1:
        clock.tick(60)
        controls()

        screen.fill((0, 0, 0))
        for i, ship in enumerate(ships):
            if not ship.dead:
                # ship.controlMove()  # used for testing collision etc
                ship.move(drawRays)
                ship.draw()
                ship.processShots()
                ship.processAsteroids()
        shipsDead = sum(ship.dead for ship in ships)
        highestScore = max([ship.score for ship in ships])
        if shipsDead == len(ships):
            population.recordData([ship.score for ship in ships])
            highestScore = max([ship.score for ship in ships])
            if highestScore > lifeHighScore:
                lifeHighScore = highestScore
            avgScore = sum([ship.score for ship in ships])/shipcount
            print(f'highestScore: {highestScore}, avgScore: {avgScore}')

            ships.sort(key=lambda x: x.score, reverse=True)
            # print(ships[0].score, ships[-1].score)
            for i, ship in enumerate(ships):
                population.population[i] = ship.net  # rearrange the nets to be in the same order as the ships
                ship.reset()
            """
            for i, ship in enumerate(ships):
                if i > 10:
                    genes = population.crossover(ships[random.randint(0, 3)].net,
                                                 ships[random.randint(0, 3)].net)
                    ship.net.connectionGenes = genes['Connections']
                    ship.net.nodeGenes = genes['Nodes']
            """
            population.repopulate()
            #   TODO: this ^ is super temporary until i can convince myself to figure out the speciation
            # population.mutateNets((1, 5), 3)
            # TODO: maybe re-sort net population based on ship score
            #  each time to allow easy easy access to the best nets
            population.finishGeneration()
        # screen.blit(font.render(f'{int(clock.get_fps())}', True, (255, 255, 255), None), (0, 0))

        ui(screen, True)
        pygame.display.update()
