from Net import Net
from random import random


class Pop:
    def __init__(self, netNum: int, inNum: int, outNum: int, connectionMutation: float, nodeMutation: float):
        """
        The init method to set up the population class

        netNum - number of nets in the training population
        inNum - number of input nodes in the population
        outNum - number of output nodes in the population
        connectionMutation - probability a connection is mutated (0-1)
        nodeMutation - probability a node is mutated (0-1)
        """
        self.netNum = netNum
        self.inNum = inNum
        self.outNum = outNum
        self.connectionMutation = connectionMutation
        self.nodeMutation = nodeMutation
        self.innovs = []
        self.population = []
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

    def mutateNets(self):
        """Randomly mutate the network via odds supplied in __init__"""
        for net in self.population:
            if random() < self.connectionMutation:
                net.connectionMutation()
            if random() < self.nodeMutation:
                net.nodeMutation()

    def getNet(self, netNum):
        """Return a reference to the net instance used to control and retrieve data from it"""
        return self.population[netNum]

    def recordData(self, data):
        """Append generation data for later analysis"""
        self.data.append(data)

    def plotGraph(self):
        pass