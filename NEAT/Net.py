import math
from random import choice, randint, random


class Net:
    def __init__(self, parent, inNum: int, outNum: int):
        """V3 neural net based of NEAT framework, must have Pop class parent from Population"""
        self.parent = parent
        self.inNum = inNum  # input node number
        self.outNum = outNum  # output node number
        self.nodeGenes = []
        self.connectionGenes = []
        self.inRange = (0, inNum - 1)
        self.outRange = (inNum, inNum + outNum - 1)
        self.populateInOut()  # populates the input and output layers with nodes
        self.fitness = 0
        self.adjustedFitness = 0
        self.species = 0

    def addNode(self, layer: int, value=0, calc=0) -> dict:
        """Add a node (dict) to the network at the specified layer (0: in, 1: hid, 2: out)"""
        self.nodeGenes.append({'nodeNum': len(self.nodeGenes),
                               'layer': layer,
                               'value': value,
                               'lastValue': value,
                               'calculated': calc})  # lasValue is used for recursive connections
        return self.nodeGenes[-1]

    def addConnection(self, inpNode: int, outNode: int, weight: float, enabled=True):
        """Add a connection gene between inpNode and outNode (represented and node numbers)"""

        self.connectionGenes.append({'innov': self.parent.checkInnov((inpNode, outNode)),
                                     'inputNode': inpNode,
                                     'outputNode': outNode,
                                     'weight': weight,
                                     'enabled': enabled})

    def populateInOut(self):
        """Create and populate the input and output layers of the net"""
        for node in range(self.inNum - 1):  # populate input layer
            self.addNode(0, 0, 2)  # nums represent layer
        self.addNode(0, 1)  # bias node that never changes
        for node in range(self.outNum):  # populate output layer
            self.addNode(1)  # 1 is the last (output) layer

    def connectionMutation(self):
        """Mutate a connection between two existing nodes"""
        inNode = randint(0, len(self.nodeGenes) - 1)
        outNode = randint(self.inNum, len(self.nodeGenes) - 1)
        if not self.parent.checkInnov((inNode, outNode)) in [gene['innov'] for gene in self.connectionGenes]:
            self.addConnection(inNode, outNode, random() * 2 - 1)

    def nodeMutation(self):
        """Add a new node to the hidden layer"""
        if len(self.connectionGenes) > 0:
            conn = choice(self.connectionGenes)
            inNode, outNode = conn['inputNode'], conn['outputNode']
            newNode = self.addNode(1)
            conn['enabled'] = False
            self.addConnection(inNode, newNode['nodeNum'], conn['weight'])
            self.addConnection(newNode['nodeNum'], outNode, 1)

    def weightMutation(self):
        for i in range(len(self.connectionGenes)):
            if rand := random() < 0.9:
                if rand < 0.45:
                    self.connectionGenes[i]['weight'] += 0.01
                else:
                    self.connectionGenes[i]['weight'] -= 0.01
            else:
                self.connectionGenes[i]['weight'] = random()*2-1
        # TODO: prevent weight exceeding range (-1,1)

    def resetNodes(self, inputList):
        for i, node in enumerate(self.nodeGenes[:self.inNum - 1]):
            self.nodeGenes[i]['value'] = inputList[i]
            # self.nodeGenes[i].pop('lastValue', None)  # test to see if this is being accessed
        # print(self.nodeGenes)
        # self.nodeGenes[self.inNum]['value'] = 1  # not really needed as bias value shouldn't change
        for node in self.nodeGenes[self.inNum:]:
            node['lastValue'] = node['value']
            node['value'] = 0
            node['calculated'] = 0

    def runNet(self, inputList: list) -> [float]:
        """Run the network and return the values of the output nodes"""

        # for nodeNum in range(self.inNum):
        #     self.nodeGenes[nodeNum]['value'] = self.sigmoid(inputList[nodeNum])
        self.resetNodes(inputList)
        self.connectionGenes.sort(key=lambda x: x['inputNode'])  # sort to run through all of in then hid

        def getValues(inpNode):  # calclist must be zero values for num of nodes
            if inpNode['calculated'] == 0:
                inpNode['calculated'] = 1
                inputnodes = [(conn['inputNode'], conn['weight']) for conn in self.connectionGenes
                              if conn['outputNode'] == inpNode['nodeNum']]
                inpNode['value'] = self.sigmoid(sum([getValues(self.nodeGenes[inp[0]]) *
                                                     inp[1] for inp in inputnodes]))
                # print(f'vals: {[(self.nodeGenes[inp[0]], inp[1]) for inp in inputnodes]}')
                inpNode['calculated'] = 2
                return inpNode['value']
            elif inpNode['calculated'] == 1:
                return inpNode['lastValue']
            elif inpNode['calculated'] == 2:
                return inpNode['value']


        for i in range(self.inNum + 1, self.inNum + self.outNum):
            # print(self.nodeGenes[i])
            getValues(self.nodeGenes[i])
            # print(self.nodeGenes[i])
        # print(self.nodeGenes)
        return  # output list
        # return self.getOut()

    def getOut(self) -> [float]:
        """Return a list populated by all node values in the outRange slice"""
        return [node['value'] for node in self.nodeGenes[self.outRange[0]:self.outRange[1] + 1]]  # beautiful

    def setScore(self, score: float):
        """Sets self.score variable to input"""
        self.fitness = score

    @staticmethod
    def sigmoid(x):
        return 1 / (1 + math.e ** (-4.9 * x))  # sigmoid func used in paper
