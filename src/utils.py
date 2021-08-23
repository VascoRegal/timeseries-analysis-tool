import numpy as np
import datetime
from statsmodels.tsa.stattools import adfuller
	
def calculate_metrics(metrics, values):
	res = {}
	n = len(values)
	
	for metric in metrics:
		if metric == 'mean':
			res[metric] = sum(values)/n
			
		elif metric == 'median':
			med = 0
			if (n % 2 == 0):
				med = (values[int(n/2)] + values[int((n/2)+1)]) / 2
			else:
				med = values[int((n+1) / 2)]
				
			res[metric] = med
	
		elif metric == 'variance':
			mean = sum(values)/n
			var = 0
			for v in values:
				var += (v - mean)**2
			var = var/n
			res[metric] = var
			
		elif metric == 'max':
			res[metric] = max(values)
		
		elif metric == 'min':
			res[metric] = min(values)	
	return res


#fitting functions

def calculate_tests(tests, x, y):
	res = {}

	for test in tests:
		if test == 'periodicity':
			res[test] = find_period(x, y)

		if test == 'stationarity':
			res[test] = is_stationary(y)

	return res

def find_period(x, y):
	return 1


def is_stationary(y, margin=0.05):
	adftest = adfuller(y, autolag='AIC')
	p = adftest[1]

	if (margin > p):
		return True
	else:
		return False
