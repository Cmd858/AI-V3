from random import choice, randint, random


class Net:
	def __init__(self, parent, inNum: int, outNum: int):
		"""V3 neural net based of NEAT framework, must have Pop class parent from Population"""
		self.parent = parent
		self.inNum = inNum  # input node number
		self.outNum = outNum  # output node number
		self.nodeGenes = []
		self.connectionGenes = []
		self.inRange = (0, inNum-1)
		self.outRange = (inNum, inNum+outNum-1)
		self.populateInOut()  # populates the input and output layers with nodes

	def addNode(self, layer: int):
		"""Add a node (dict) to the network at the specified layer (0: in, 1: hid, 2: out)"""
		self.nodeGenes.append({'nodeNum': len(self.nodeGenes),
											   'layer': layer,
											   'value': 0})  # value to be used later
		return self.nodeGenes[-1]

	def addConnection(self, inpNode: int, outNode: int, weight: float):
		"""Add a connection gene between inpNode and outNode (represented and node numbers)"""

		self.connectionGenes.append({'innov': self.parent.checkInnov((inpNode, outNode)),
														   'inputNode': inpNode,
														   'outputNode': outNode,
														   'weight': weight,
														   'enabled': True})

	def populateInOut(self):
		"""Create and populate the input and output layers of the net"""
		for node in range(self.inNum):  # populate input layer
			self.addNode(0)  # nums represent layer
		for node in range(self.outNum):  # populate output layer
			self.addNode(1)  # 1 is the last (output) layer

	def connectionMutation(self):
		"""Mutate a connection between two existing nodes"""
		attempts = 1
		for attempt in range(attempts):
			if not randint(0, 1) or self.inNum + self.outNum >= len(self.nodeGenes):
				# bool choice of in -> hid or out (1), hid -> out (0), checks if any hidden nodes are available
				node1 = randint(*self.inRange)
				node2 = randint(self.outRange[0], self.outRange[0] + len(self.connectionGenes))
				# ^ equal chance between hid and out nodes
			else:
				node1 = randint(self.outRange[1] + 1, self.outRange[1] + len(self.connectionGenes))
				node2 = randint(*self.outRange)  # possible to have in lower than out due to number semantics
			if not (node1, node2) in self.connectionGenes:
				self.addConnection(node1, node2, random() * 2 - 1)
				break

	def nodeMutation(self):
		"""Add a new node to the hidden layer"""
		attempts = 5
		for attempt in range(attempts):
			con = choice(self.connectionGenes)
			if (self.inRange[0] < con['inputNode'] < self.inRange[1] and
					self.outRange[0] < con['outputNode'] < self.outRange[1]):
				newNode = self.addNode(1)
				con['enabled'] = False  # disable original connection as it is being erased
				self.addConnection(con['inputNode'], newNode['nodeNum'], con['weight'])
				self.addConnection(newNode['nodeNum'], con['outputNode'], 1)  # overall weight not changed
				break

	def runNet(self, inputList: list):
		"""Run the network and return the values of the output nodes"""
		for nodeNum in range(self.inNum):
			self.nodeGenes[nodeNum]['value'] = inputList[nodeNum]
		self.connectionGenes.sort(key=lambda x: x['inputNode'])  # sort to run through all of in then hid
		for connection in self.connectionGenes:  # gets connection dict
			inNode = connection['inputNode']
			outNode = connection['outputNode']  # temp vars to avoid messy one-liner
			weight = connection['weight']
			self.nodeGenes[outNode]['value'] += self.nodeGenes[inNode]['value'] * weight
		return self.getOut()

	def getOut(self):
		"""Return a list populated by all node values in the outRange slice"""
		return [node['value'] for node in self.nodeGenes[self.outRange[0]:self.outRange[1]+1]]  # beautiful
