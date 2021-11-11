from Population import Pop
import Graphing
from random import random


def testPopulation():
	testPop = Pop(10, 4, 4, 1, 0, 1)
	testPop.populate()
	print('Populated')
	for i in range(5):
		testPop.mutateNets()
	print('Mutated')
	for i in range(10):
		net = testPop.getNetRun(i)
		print(net.runNet([4, 5, 6, 7]))
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
	netOut = []
	for i in range(80):  # 80 generations
		netOut.append([])
		for j in range(50):  # 50 nets per generation
			netOut[i].append(random() * 5 + i * 0.1)
	Graphing.plotData(netOut)


if __name__ == '__main__':
	testPopulation()
	testGraphing()
