import matplotlib
import matplotlib.pyplot as plt
import numpy as np
matplotlib.use('GTK3Agg')

from utils import TIME_CONVERSION_TABLE

def gen_plot(x, y, xlabel, ylabel, title, window, **kwargs):
	plt.figure(window)
	plt.plot(x,y, **kwargs)
	plt.xlabel(xlabel)
	plt.ylabel(ylabel)
	plt.title(title)
	
def gen_hist(x, bins, xlabel, ylabel, title, window, unit='second', **kwargs):
	plt.figure(window)
	hst, edges = np.histogram(x, bins)

	plt.bar(range(len(hst)), hst, tick_label=
			[f'{bins[i] / TIME_CONVERSION_TABLE[unit], bins[i+1] / TIME_CONVERSION_TABLE[unit]}' for i,j in enumerate(hst)], **kwargs)

	plt.xlabel(xlabel)
	plt.ylabel(ylabel)
	plt.title(title)
	
def show_plots():
	for i in plt.get_fignums():
		plt.figure(i)
		plt.legend()
	plt.show()
