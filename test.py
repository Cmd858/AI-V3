from Population import Pop
import Graphing
from random import random

if __name__ == '__main__':
	testPop = Pop(1, 2, 2, 1, 0)
	testPop.populate()
	testPop.mutateNets()
	testPop.mutateNets()
	net = testPop.getNet(0)
	print(net.runNet([4, 5]))
	netOut = []
	for i in range(80):  # 80 generations
		netOut.append([])
		for j in range(50):  # 50 nets per generation
			netOut[i].append(random()*5 + i * 0.1)
	Graphing.plotData(netOut)
