import numpy as np
from datetime import datetime
from statsmodels.tsa.stattools import adfuller
from scipy.stats import pearsonr

'''	
Tabela para conversão de valores.
O campo timeIntervalsUnit é uma key desta varável.
'''
TIME_CONVERSION_TABLE = {'second': 1,
				   'minute': 60,
                   'hour': 3600,
                   'day': 86400,
                   'week': 604800,
                   'month': 2629743.83,
                   'year': 31556926}



def calculate_metrics(metrics, values):
	'''
	Calcula as métricas desejadas.

	Params:
		(list) metrics	->	strings com os nomes das métricas a calcular
		(list) values	->	dataset a analisar

	Return:
		(dict) res		->  dicionario com os resultados, {métrica: resultado} 

	'''
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

		elif metric == 'outra_metrica_a_ser_adicionada':
			pass

	return res

def calculate_tests(tests, x, y):
	'''
	Calcula os testes desejados.

	Params:
		(list) tests	->	strings com os nomes dos testes a calcular
		(list) x		->	eixo x do dataset
		(list) y		-> 	eixo y

	Return:
		(dict) res		->  dicionario com os resultados, {teste: resultado} 

	'''

	res = {}

	for test in tests:
		if test == 'periodicity':
			res[test] = autocorrelate(x, y) 

		elif test == 'stationarity':
			res[test] = is_stationary(y)

		elif test == 'outro_teste_qualquer':
			pass

	return res


def get_sample_frequency(x, y):
	'''
	Calcula a frequencia de amostragem
	'''
	start = datetime.timestamp(min(x))
	end = datetime.timestamp(max(x))

	fs = len(y) / (end - start)

	return fs


def autocorrelate(time, vals):
	'''
	Implementação do algoritmos de autocorrelação para descobrir o período

	Nota: Embora tenha aplicado o algoritmo bem, acho que estou a interpretar mal a converter
		  os resultados para segundos (o output do algoritmo dá um valor de r e um de lag apenas)

	Params:
		(list) time	-> valores do tempo
		(list) vals	-> dataset

	Return:
		(int/float) -> período em segundos
	'''
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
	'''
	Implementação de Augmented Dickey-Fuller test

	Param:
		(list) 	y		->	dataset
		(float)	margin	->	margem do algoritmo do adfuller

	Return:
		(bool)	->	se é stationary ou não
	'''

	adftest = adfuller(y, autolag='AIC')
	p = adftest[1]

	if (margin > p):
		return True
	else:
		return False

def test_causality(y1, y2):
	'''
	Implementação do algorimto de Pearson. Dados 2 datasets, retorna um valor entre -1 e 1.
	Próximo de 0 significa que não há coorelação entre valores.
	Próximo de -1 significa uma proporcionalidade inversa.
	Próximo de 1 significa uma proporcionalidade direta. 

	Param:
		(list)	y1	->	dataset 1
		(list)	y2	->	dataset 2

	Return:
		(float)	corr	->	indice da correlação (entre -1 e 1)
	'''

	if len(y1) > len(y2):
		y1 = y1[:len(y2)]
	else:
		y2 = y2[:len(y1)]


	corr, _ = pearsonr(y1, y2)
	return corr

def calculate_bucket(lst):
	'''
	Função usada para transformar num numpy array os intervalos de valores passados no config,
	sejam eles no formato "from: to:" ou escrito em extenso

	Param:
		(list)	lst	->	intervalo inputted

	Return:
		(numpy array)	->	numpy array com os intervalos formatados		
	'''
	if type(lst) == dict:
		return np.arange(lst['from'], lst['to'], lst['interval'])
	else:
		res = []
		for l in lst:
			for i in l:
				res.append(i)
		return np.array(list(dict.fromkeys(res)))



