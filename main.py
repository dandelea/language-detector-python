import collections, numpy, operator, pandas, re

from preprocessing import idioms, Dictionary, restore

def split_in_words(sentence):
	return re.findall(r"[\w']+", sentence)

def summary(word):
	result = {}
	for idiom in idioms:
		d = dictionaries[idiom]
		result[idiom] = d.value(word)
	return result

def is_perfect(word):
	aux = summary(word)
	if sum(x==0.0 for x in aux.values())==len(idioms)-1:
		return [k for k, v in aux.items() if v!=0.0][0]
	else:
		return None

def method1(query):
	"""Suma de los valores"""
	words = split_in_words(query)
	score = {}
	for idiom in idioms:
		v = 0.0
		d = dictionaries[idiom]
		for word in words:
			aux = d.value(word)
			v = v+aux
		score[idiom] = v
	return max(score.items(), key=operator.itemgetter(1))[0]

def method2(query):
	"""Idioma mayoritario en la frase"""
	words = split_in_words(query)
	score = {}
	for idiom in idioms:
		score[idiom] = 0
	for word in words:
		max_idiom = max(summary(word).items(), key=operator.itemgetter(1))[0]
		score[max_idiom] = score[max_idiom]+1
	return max(score.items(), key=operator.itemgetter(1))[0]

def method3(query):
	"""Mayor número de perfectos"""
	words = split_in_words(query)
	score = {}
	for idiom in idioms:
		score[idiom] = 0
	for word in words:
		aux = is_perfect(word)
		if aux:
			score[aux] = score[aux] + 1
	return max(score.items(), key=operator.itemgetter(1))[0]


def matrix(method):
	disp = collections.defaultdict(dict)

	for idiom1 in idioms:
		for idiom2 in idioms:
			disp[idiom1][idiom2] = 0.0

	# Conteo

	for idiom in idioms:
		d = dictionaries[idiom]
		for sentence in d.test:
			disp[d.idiom][method(sentence)] += 1


	# Pasarlo a tabla

	N = len(idioms)
	matrix = numpy.zeros((N, N))
	for i in range(N):
		for j in range(N):
			matrix[i,j] = disp[idioms[i]][idioms[j]]

	# Porcentajes

	suma = numpy.sum(matrix, axis=0)
	for i in range(N):
		for j in range(N):
			matrix[i,j] = matrix[i,j]*100/suma[i]

	return matrix


if __name__=='__main__':
	dictionaries = restore(input("Filepath: "))
	m = matrix(method3)
	dataframe = pandas.DataFrame(m, index=idioms, columns=idioms)
	print()
	print(dataframe)
	print()