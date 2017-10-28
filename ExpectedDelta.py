import numpy as np
from matplotlib import pyplot as plt

def my_func(mu, sigma, size):
	return 1/(sigma*np.sqrt(2*np.pi))*np.exp(-(size-mu)**2 / (2*sigma**2) )

def plotfunc():
	mu, sigma = 1, 10
	x = np.arange(0,4)
	print len(x)
	p = my_func(mu, sigma, x)
	plt.plot(x,p)
	plt.show()

def main():
	plotfunc()

if __name__ == '__main__':
	main()