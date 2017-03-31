import datetime, nltk, pickle, random, re

def split_training_test(idiom, percent_test):
	with open(idiom+'.txt', 'rt', encoding = "utf-8") as f:
		raw_text = f.read()
	tokenizer = nltk.data.load("tokenizers/punkt/"+idiom+".pickle")
	sentences = tokenizer.tokenize(raw_text)
	sentences = [sentence.replace('\n',' ') for sentence in sentences]
	N = int(percent_test * len(sentences) * 0.01)
	test_sample = random.sample(sentences, N)
	training_sample = [x for i,x in enumerate(sentences) if i not in test_sample]
	return {"training": training_sample, "test": test_sample}

idioms = ['spanish', 'english', 'french', 'portuguese', 'italian', 'danish', 'dutch']

class Dictionary():
	def __init__(self, idiom, percent_test):
		self.idiom = idiom
		self.percent_test = percent_test
		split = split_training_test(idiom, percent_test)
		self.training = split['training']
		self.test = split['test']
		self.training_size = len(self.training)
		self.test_size = len(self.test)

	def value(self, word):
		if word in self.probability:
			return self.probability[word]
		else:
			return 0.0

	def pre_store(self, values):
		self.probability = values

####

def value(word, word_list):
	return word_list.count(word) / float(len(word_list))

def bag_of_words(idioms):
	words_set = set()
	for idiom in idioms:
		with open(idiom+'.txt', 'rt', encoding = "utf-8") as f:
			raw_text = f.read()
		word_list = re.findall(r"[\w']+", raw_text)
		vocabulary = set(word_list)
		words_set = words_set.union(vocabulary)
	return words_set

def pickle_to_save(idioms, percent_test=10):
	dictionaries = {}
	bag_words = bag_of_words(idioms)
	for idiom in idioms:
		r = {}
		dictionary = Dictionary(idiom, percent_test)
		word_list = [word for sentence in dictionary.training for word in sentence.split()]
		for word in bag_words:
			r[word] = value(word, word_list)
		dictionary.pre_store(r)
		dictionaries[idiom] = dictionary
		print("COMPLETED Parsing " + idiom + " language...\r")
	return dictionaries

def run(filepath):
	"""Run the preprocessing routine.
	"""
	p = pickle_to_save(idioms)
	# Save pickle
	output = open(filepath, 'wb')
	pickle.dump(p, output)
	output.close()

def restore(filepath):
	pkl = open(filepath, 'rb')
	obj = pickle.load(pkl)
	pkl.close()
	return obj

if __name__=='__main__':
	run("data.pkl")
