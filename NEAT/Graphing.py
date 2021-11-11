import matplotlib.pyplot as plt
import numpy as np


def plotData(data):
	avg = []
	r = np.arange(0, len(data), 1)
	fig, ax = plt.subplots()
	i = 0
	for dataList in data:
		avg.append(sum(dataList)/len(dataList))
		ax.scatter(np.full(len(dataList), i), dataList, 2)
		i += 1
	ax.plot(r, avg)
	plt.show()
