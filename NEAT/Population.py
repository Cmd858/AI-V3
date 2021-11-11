from NEAT import Graphing
from NEAT.Net import Net
from random import random, randint


class Pop:
	def __init__(self,
				 netNum: int,
				 inNum: int,
				 outNum: int,
				 connectionMutation: float,
				 nodeMutation: float,
				 crossoverNum: int):
		"""
		The init method to set up the population class

		netNum - number of nets in the training population
		inNum - number of input nodes in the population
		outNum - number of output nodes in the population
		connectionMutation - probability a connection is mutated (0-1)
		nodeMutation - probability a node is mutated (0-1)
		crossoverNum - number of attempts at crossover
		"""
		self.netNum = netNum
		self.inNum = inNum
		self.outNum = outNum
		self.connectionMutation = connectionMutation
		self.nodeMutation = nodeMutation
		self.crossoverNum = crossoverNum
		self.innovs = []
		self.population: list[Net] = []
		self.results = []
		self.data = []  # used to store scoring data for analysis each generation

	def populate(self):
		"""Populate the class with the required number of nets"""
		for net in range(self.netNum):
			self.population.append(Net(self, self.inNum, self.outNum))

	def checkInnov(self, inOutTuple):
		"""Return the innov number of a connection and add that connection if it doesn't exist"""
		if inOutTuple in self.innovs:
			return self.innovs.index(inOutTuple)
		else:
			self.innovs.append(inOutTuple)
			return len(self.innovs)-1  # -1 bc last innov is always 1 less than list length

	def mutateNets(self, start=0):
		"""Randomly mutate the network via odds supplied in __init__"""
		for net in self.population[start:]:  # slice of list to mutate
			if random() < self.connectionMutation:
				net.connectionMutation()
			if random() < self.nodeMutation:
				net.nodeMutation()

	def getNetRun(self, netNum: int) -> Net:
		"""Return a reference to the net instance's runNet function for running from a controller class"""
		return self.population[netNum].runNet

	def recordData(self, data):
		"""Append generation data for later analysis"""
		self.data.append(data)

	def plotGraph(self):
		"""Plot generational data using the graphing module"""
		Graphing.plotData(self.data)

	def crossover(self, net1: Net, net2: Net):
		"""Crossover two nets to create a new superior net"""
		newConnections = {'Connections': [], 'Nodes': []}
		innovs1 = [gene['innov'] for gene in net1.connectionGenes]  # get nums in list
		innovs2 = [gene['innov'] for gene in net2.connectionGenes]
		for innov in range(len(self.innovs)):
			if innov in innovs1 and innov in innovs2:
				if randint(0, 1):  # bool True or False = 50% chance for each gene
					gene = net1.connectionGenes[innovs1.index(innov)]
					newConnections['Connections'].append(gene)
					newConnections['Nodes'].append(net1.nodeGenes[gene['inputNode']])
					newConnections['Nodes'].append(net1.nodeGenes[gene['outputNode']])
				else:
					gene = net2.connectionGenes[innovs2.index(innov)]
					newConnections['Connections'].append(gene)
					newConnections['Nodes'].append(net2.nodeGenes[gene['inputNode']])
					newConnections['Nodes'].append(net2.nodeGenes[gene['outputNode']])
			elif innov in innovs1 or innov in innovs2:
				if innov in innovs1:
					gene = net1.connectionGenes[innovs1.index(innov)]
					newConnections['Connections'].append(gene)
					newConnections['Nodes'].append(net1.nodeGenes[gene['inputNode']])
					newConnections['Nodes'].append(net1.nodeGenes[gene['outputNode']])
				else:
					gene = net2.connectionGenes[innovs2.index(innov)]
					newConnections['Connections'].append(gene)
					newConnections['Nodes'].append(net2.nodeGenes[gene['inputNode']])
					newConnections['Nodes'].append(net2.nodeGenes[gene['outputNode']])
		returnList = []
		for gene in newConnections['Nodes']:
			if gene not in returnList:
				returnList.append(gene)
		newConnections['Nodes'] = returnList
		return newConnections

	def repopulate(self, nets: list[list[dict]]):
		"""Overwrite the genes in net instances to avoid recreation"""
		# TODO: finish repopulation logic

	def getFitness(self):
		"""Return fitness list for all nets in order"""
		# TODO: complete fitness algorithm
		return []

	def finishGeneration(self):
		attempts = []  # indexes of parent nets
		for attempt in range(self.crossoverNum):

			pass  # TODO: iterate nets and push new genes in
		self.repopulate(self.population)
