class NaiveBayesClassifier(object):
	"""Naive Bayes classifier implementation for a bag of words

	Attributes:
		num_classes - the number of classes to classify
		frequency_list - a list of arrays with words frequencies
		class_distrib - a list of log priors of each class label
	"""
	def __init__(self, num_classes, num_words):
		super(NaiveBayesClassifier, self).__init__()
		self.num_classes = num_classes
		self.frequency_list = [[1 for j in range(num_words)] for i in range(num_classes)]
		self.priors = []