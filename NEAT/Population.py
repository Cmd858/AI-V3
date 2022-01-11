# from NEAT import Graphing  # not in 3.10 yet
from NEAT.Net import Net
from random import random, randint


class Pop:
    def __init__(self,
                 netNum: int,
                 inNum: int,
                 outNum: int,
                 connectionMutation: float,
                 nodeMutation: float,
                 weightMutation: float,
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
        self.inNum = inNum + 1  # add space for bias node
        self.outNum = outNum
        self.connectionMutation = connectionMutation
        self.nodeMutation = nodeMutation
        self.weightMutation = weightMutation
        self.crossoverNum = crossoverNum
        self.innovs = []
        self.population: list[Net] = []
        self.species = []
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
            return len(self.innovs) - 1  # -1 bc last innov is always 1 less than list length

    def mutateNets(self, mutationRange, start=0):
        """Randomly mutate the network via odds supplied in __init__"""
        # TODO: reference paper to make mutation the same as example
        for net in self.population[start:]:  # slice of list to mutate
            for i in range(randint(*mutationRange)):
                if random() < self.weightMutation:
                    # TODO: fix this from reducing highest score bc like wtf how?
                    # net.weightMutation()
                    pass
                if random() < self.connectionMutation:
                    net.connectionMutation()
                if random() < self.nodeMutation:
                    net.nodeMutation()

    def getNetRun(self, netNum: int):
        """Return a reference to the net instance's runNet function for running from a controller class"""
        return self.population[netNum].runNet

    def recordData(self, data):
        """Append generation data for later analysis"""
        self.data.append(data)

    def plotGraph(self):
        """Plot generational data using the graphing module"""

    # Graphing.plotData(self.data)

    def crossover(self, net1: Net, net2: Net):
        """
        Crossover two nets to create a new superior net

        Implements the crossover algorithm in NEAT, which will pick randomly with matching genes and
        only take disjoint and excess genes for the more fit parent
        """
        net1fitness = net1.fitness
        net2fitness = net2.fitness
        newConnections = {'Connections': [], 'Nodes': []}
        innovs1 = [gene['innov'] for gene in net1.connectionGenes]  # get nums in list
        innovs2 = [gene['innov'] for gene in net2.connectionGenes]
        for innov in range(len(self.innovs)):
            if innov in innovs1 and innov in innovs2:
                if randint(0, 1):  # bool True or False = 50% chance for each gene
                    gene = net1.connectionGenes[innovs1.index(innov)]
                    newConnections['Connections'].append(gene)
                else:
                    gene = net2.connectionGenes[innovs2.index(innov)]
                    newConnections['Connections'].append(gene)
            elif innov in innovs1 or innov in innovs2:
                if innov in innovs1 and net1fitness > net2fitness:
                    gene = net1.connectionGenes[innovs1.index(innov)]
                    newConnections['Connections'].append(gene)
                elif innov in innovs2 and net1fitness < net2fitness:
                    gene = net2.connectionGenes[innovs2.index(innov)]
                    newConnections['Connections'].append(gene)
        returnList = []
        nodeNums1 = {*[node['nodeNum'] for node in net1.nodeGenes]}
        nodeNums2 = {*[node['nodeNum'] for node in net2.nodeGenes]}
        # check if in both or one then random add
        # print(nodeNums1)
        # print(nodeNums2)
        for i in range(max(nodeNums1 | nodeNums2) + 1):
            if i in nodeNums1 and i in nodeNums2:
                if randint(0, 1):
                    returnList.append(next(item for item in net1.nodeGenes if item['nodeNum'] == i))
                else:
                    returnList.append(next(item for item in net2.nodeGenes if item['nodeNum'] == i))
            elif i in nodeNums1 or i in nodeNums2:
                if i in nodeNums1:
                    returnList.append(next(item for item in net1.nodeGenes if item['nodeNum'] == i))
                else:
                    returnList.append(next(item for item in net2.nodeGenes if item['nodeNum'] == i))
        newConnections['Nodes'] = returnList
        # print(newConnections)
        return newConnections

    def repopulate(self, nets: list[Net]):
        """Overwrite the genes in net instances to avoid recreation"""
        # TODO: apply speciation here and maybe rename the func
        excessCoef = 1
        disjointCoef = 1  # standard coefficients (p13)
        avgWeightCoef = 0.4
        deltaT = 3  # speciation threshold

        def getDelta(connections1, connections2):
            N = 1  # should be num genes for count of more than about 20
            matching = 0
            excess = 0
            disjoint = 0
            weightDifSum = 0
            net1innovs = [connection['innov'] for connection in connections1]
            net2innovs = [connection['innov'] for connection in connections2]
            allinnovs = net1innovs + net2innovs
            excessThreshold = min(max(net1innovs), max(net2innovs))  # the max number that can be disjoint
            for i in range(max(allinnovs)):
                count = allinnovs.count(i)
                if count == 2:
                    matching += 1
                    weightDifSum += abs(connections1[i]['weight'] -  # used to calculate the average weight difference
                                        connections2[allinnovs.index(i, i+1)-len(connections1)]['weight'])
                elif count == 1:
                    if i <= excessThreshold:
                        disjoint += 1
                    else:
                        excess += 1
            avgWeight = weightDifSum / matching  # average weight difference of matching genes
            return excessCoef*excess/N + disjointCoef*disjoint/N + avgWeightCoef * avgWeight

        def adjustFitness(net):
            adjustedFitness = net.fitness/sum([deltaT > getDelta(net.connectionGenes,  # sh func (pg13)
                                                        x.connectionGenes) for x in self.population])
            return adjustedFitness

        for net in self.population:
            net.adjustedFitness = adjustFitness(net)
        # TODO: figure out how to crossover some of the best nets
        #  and what threshold to have for getting rid of the worst nets
        # the next section will be guesswork based on the paper as I can't find info on this bit
        # this is the bit when bad networks are culled and good networks are bred
        # the amount of each this happens to is a complete guess





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
