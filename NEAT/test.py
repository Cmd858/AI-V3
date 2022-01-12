from Population import Pop
import Graphing
from random import random, randint


def testPopulation():
    testPop = Pop(10, 4, 4, 1, 0, 0, 1)
    testPop.populate()
    print('Populated')
    for i in range(5):
        testPop.mutateNets((1, 1))
    print('Mutated')
    for i in range(10):
        net = testPop.population[i]
        net.runNet([4, 5, 6, 7])
        print(net.getOut())
    newNet = testPop.crossover(testPop.population[0], testPop.population[1])
    newNet['Connections'].sort(key=lambda x: x['innov'])
    testPop.population[0].connectionGenes.sort(key=lambda x: x['innov'])
    testPop.population[1].connectionGenes.sort(key=lambda x: x['innov'])
    newNet['Nodes'].sort(key=lambda x: x['nodeNum'])
    print(newNet['Connections'])
    print(testPop.population[0].connectionGenes)
    print(testPop.population[1].connectionGenes)
    print(newNet['Nodes'])
    print(testPop.population[0].nodeGenes)
    print(testPop.population[1].nodeGenes)


def testGraphing():
    data = []
    for j in range(50):
        netScores = [randint(1, 1000) for _ in range(100)]
        print(netScores)
        highestScore = max(netScores)
        avgScore = sum(netScores) / len(netScores)
        stdDeviation = (sum((avgScore - score) ** 2 for score in netScores) / len(netScores)) ** 0.5
        data.append({'scores': netScores,
                     'highestScore': highestScore,
                     'avgScore': avgScore,
                     'stdDeviation': stdDeviation})
    Graphing.plotData(data)


if __name__ == '__main__':
    testPopulation()
    testGraphing()
