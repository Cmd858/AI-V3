from Population import Pop
import Graphing
from random import random


def testPopulation():
	testPop = Pop(10, 4, 4, 1, 0)
	testPop.populate()
	for i in range(5):
		testPop.mutateNets()
	for i in range(10):
		net = testPop.getNetRun(i)
		print(net.runNet([4, 5, 6, 7]))
	print(testPop.crossover(testPop.population[0], testPop.population[1]))
	print(testPop.population[0].connectionGenes)
	print(testPop.population[1].connectionGenes)


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
