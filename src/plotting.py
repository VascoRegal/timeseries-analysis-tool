import matplotlib.pyplot as plt

def gen_plot(x, y, xlabel, ylabel, title, window, **kwargs):
	plt.figure(window)
	plt.plot(x,y, **kwargs)
	plt.xlabel(xlabel)
	plt.ylabel(ylabel)
	plt.title(title)
	
def gen_hist(x, xlabel, ylabel, title, window, **kwargs):
	plt.figure(window)
	plt.hist(x, **kwargs)
	plt.xlabel(xlabel)
	plt.ylabel(ylabel)
	plt.title(title)
	
def show_plots():
	for i in plt.get_fignums():
		plt.figure(i)
		plt.legend()
	plt.show()
