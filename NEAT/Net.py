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
        for node in range(self.inNum-1):  # populate input layer
            self.addNode(0, 0, 2)  # nums represent layer
        self.addNode(0, 1)  # bias node that never changes
        for node in range(self.outNum):  # populate output layer
            self.addNode(1)  # 1 is the last (output) layer

    def connectionMutation(self):
        """Mutate a connection between two existing nodes"""
        attempts = 1
        for attempt in range(attempts):
            if not randint(0, 1) or self.inNum + self.outNum >= len(self.nodeGenes):
                # bool choice of in -> hid or out (1), hid -> out (0), checks if any hidden nodes are available
                node1 = randint(*self.inRange)
                node2 = randint(self.outRange[0], len(self.nodeGenes) - 1)
            # ^ equal chance between hid and out nodes
            else:
                node1 = randint(self.outRange[1] + 1, len(self.nodeGenes) - 1)
                node2 = randint(*self.outRange)  # possible to have in lower than out due to number semantics
            if not self.parent.checkInnov((node1, node2)) in self.connectionGenes:
                self.addConnection(node1, node2, random() * 2 - 1)
                break

    def nodeMutation(self):
        """Add a new node to the hidden layer"""
        attempts = 5
        if len(self.connectionGenes) != 0:
            for attempt in range(attempts):
                con = choice(self.connectionGenes)
                # print(self.connectionGenes)
                # print(con)
                if (self.inRange[0] < con['inputNode'] < self.inRange[1] and
                        self.outRange[0] < con['outputNode'] < self.outRange[1]):
                    newNode = self.addNode(1)
                    con['enabled'] = False  # disable original connection as it is being erased
                    self.addConnection(con['inputNode'], newNode['nodeNum'], con['weight'])
                    self.addConnection(newNode['nodeNum'], con['outputNode'], 1)  # overall weight not changed
                    break

    def resetNodes(self, inputList):
        print(self.nodeGenes)
        for i, node in enumerate(self.nodeGenes[:self.inNum-1]):
            node['value'] = inputList[i]
        print(self.nodeGenes)
        # self.nodeGenes[self.inNum]['value'] = 1  # not really needed as bias value shouldn't change
        for node in self.nodeGenes:
            node['lastValue'] = node['value']
            node['value'] = 0
            node['calculated'] = 0

    def runNet(self, inputList: list) -> [float]:
        """Run the network and return the values of the output nodes"""

        # for nodeNum in range(self.inNum):
        #     self.nodeGenes[nodeNum]['value'] = self.sigmoid(inputList[nodeNum])
        # TODO: ^ make it use sigmoid on hidden and out after rejig
        # TODO: make it use resetNodes and add recursivness maybe
        self.resetNodes(inputList)
        self.connectionGenes.sort(key=lambda x: x['inputNode'])  # sort to run through all of in then hid

        def getValues(inpNode):  # calclist must be zero values for num of nodes
            if inpNode['calculated'] == 0:
                inpNode['calculated'] = 1
                inputnodes = [(conn['inputNode'], conn['weight']) for conn in self.connectionGenes
                              if conn['outputNode'] == inpNode['nodeNum']]
                inpNode['value'] = sum([getValues(self.nodeGenes[inp[0]]) *
                                        inp[1] for inp in inputnodes])
                inpNode['calculated'] = 2
                return inpNode['value']
            elif inpNode['calculated'] == 1:
                return inpNode['oldValue']
            elif inpNode['calculated'] == 2:
                return inpNode['value']

            # TODO: this code should work but must update self not internal variable as it does
            #  not persist causing no movement
        for i in range(self.inNum+1, self.inNum+self.outNum):
            getValues(self.nodeGenes[i])
        print(self.nodeGenes)

        """
        for connection in self.connectionGenes:  # gets connection dict
            inNode = connection['inputNode']
            outNode = connection['outputNode']  # temp vars to avoid messy one-liner
            weight = connection['weight']
            self.nodeGenes[outNode]['value'] += self.nodeGenes[inNode]['value'] * weight
        """
        # TODO: redesign this to deal with recurrent and backwards connections like 5 <- 5 or 6 <- 8
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
        return 1/(1+math.e ** (-4.9 * x))  # sigmoid func used in paper
