import matplotlib.pyplot as plt
import numpy as np


def plotData(data):
	"""
	avg = []
	r = np.arange(0, len(data), 1)
	fig, ax = plt.subplots()
	i = 0
	for dataList in data:
		avg.append(sum(dataList)/len(dataList))
		ax.scatter(np.full(len(dataList), i), dataList, 2)
		i += 1
	"""
	fig, ax = plt.subplots()
	highest, avg, stdDisthigh, stdDistlow = [], [], [], []
	for i in range(len(data)):
		ax.scatter(np.full(len(data[i]['scores']), i), data[i]['scores'], 2)
		highest.append(data[i]['highestScore'])
		avg.append(data[i]['avgScore'])
		stdDisthigh.append(avg[-1] + data[i]['stdDeviation'])
		stdDistlow.append(avg[-1] - data[i]['stdDeviation'])
	ax.plot(highest)
	ax.plot(avg)
	ax.plot(stdDisthigh)
	ax.plot(stdDistlow)
	plt.show()

