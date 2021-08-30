import numpy as np
from datetime import datetime
from statsmodels.tsa.stattools import adfuller
from scipy.stats import pearsonr
	

TIME_CONVERSION_TABLE = {'second': 1,
				   'minute': 60,
                   'hour': 3600,
                   'day': 86400,
                   'week': 604800,
                   'month': 2629743.83,
                   'year': 31556926}

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
			dev = [(x - mean) ** 2 for x in values]
			var = sum(dev)/n
			res[metric] = var
			
		elif metric == 'max':
			res[metric] = max(values)
		
		elif metric == 'min':
			res[metric] = min(values)	
	return res

def calculate_tests(tests, x, y):
	res = {}

	for test in tests:
		if test == 'periodicity':
			res[test] = autocorrelate(x, y) 

		if test == 'stationarity':
			res[test] = is_stationary(y)

	return res

def get_sample_frequency(x, y):
	start = datetime.timestamp(min(x))
	end = datetime.timestamp(max(x))

	fs = len(y) / (end - start)

	return fs


def autocorrelate(time, vals):
	n = len(vals)
	fs = get_sample_frequency(time, vals)
	mean = sum(vals)/n
	norm = [v - mean for v in vals]
	res = np.correlate(norm, norm, mode='same')
	acorr = res[n//2 + 1:] / (calculate_metrics(['variance'], norm)['variance'] * np.arange(n-1, n//2, -1))

	lag = np.abs(acorr).argmax() + 1
	r = acorr[lag - 1]

	if np.abs(r) > 0.5:
		return (lag / fs)
	
	return 0

def is_stationary(y, margin=0.05):
	adftest = adfuller(y, autolag='AIC')
	p = adftest[1]

	if (margin > p):
		return True
	else:
		return False

def test_causality(y1, y2):
	if len(y1) > len(y2):
		y1 = y1[:len(y2)]
	else:
		y2 = y2[:len(y1)]


	corr, _ = pearsonr(y1, y2)
	return corr

def calculate_bucket(lst):
	if type(lst) == dict:
		return np.arange(lst['from'], lst['to'], lst['interval'])
	else:
		res = []
		for l in lst:
			for i in l:
				res.append(i)
		return np.array(list(dict.fromkeys(res)))



