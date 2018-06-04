import naivebayes as nb
import numpy as np
import string


# Constants
FILE_DIR = "./"
TRAINING_FNAME = "trainingSet.txt"
TESTING_FNAME = "testSet.txt"
PP_TRAIN_FNAME = "preprocessed_train.txt"
PP_TEST_FNAME = "preprocessed_test.txt"
RESULTS_FNAME = "results.txt"


def main():

	# Load in raw data from txt file
	print("Loading in raw data...")
	raw_training_data = load_data(TRAINING_FNAME)
	raw_testing_data = load_data(TESTING_FNAME)

	# Preprocess the data into a bag of words and feature vectors
	print("Processing data into bag of words...")
	bag = build_bag(np.vstack((raw_training_data, raw_testing_data)))
	X_train, y_train = build_fvectors(bag, raw_training_data)
	X_test, y_test = build_fvectors(bag, raw_testing_data)
	preprocess_summary(bag, X_train, y_train, X_test, y_test)

	# Train Naive Bayes classifier and output accuracy on test set
	print("Training NB classifier...")
	clf = train(bag, X_train, y_train)
	print("Testing NB classifier on training set...")
	train_res = test(clf, X_train, y_train)
	print("Testing NB classifier on testing set...")
	test_res = test(clf, X_test, y_test)
	print("Saving results...")
	summary(train_res, test_res)
	print("Done.")

def load_data(fn):
	"""Loads sentences and label

	Args:
		fn - the filename of a textfile to read in

	Returns:
		a numpy array of 2-tuples with a list of words and the label
	"""
	data = []
	with open(FILE_DIR + fn, "r") as f:

		for line in f.readlines():

			sample = line.split()

			# Strip punctuation from sentence
			for i in range(len(sample)):

				sample[i] = "".join(
					l for l in sample[i] if l not in string.punctuation)

			data.append((sample[:-1], int(sample[-1])))

	return np.array(data)

def build_bag(data):
	"""Builds a bag of words from all words existing in raw data

	Args:
		data - raw data of all sentences that will be loaded into the bag

	Returns:
		a list of words in alphabetical order, no dupes
	"""
	bag = []
	for sample in data:

		bag += [word.lower() for word in sample[0] if word not in bag and len(word) > 0]

	# Set the list to insure all dupes are removed
	bag = list(set(bag))
	bag.sort()
	return bag

def build_fvectors(bag, data):
	"""Creates a feature vector given a bag of words and some raw sentence data

	Args:
		bag - bag of words
		data - list of samples of sentences

	Returns:
		formal vector list of features and corresponding list of labels
	"""
	X, y = [], []
	for sample in data:

		sample_vector = []

		for word in bag:

			sample_vector += [1] if word in sample[0] else [0] 

		X.append(sample_vector)
		y.append(sample[1])

	return X, y

def preprocess_summary(bag, X_train, y_train, X_test, y_test):
	"""Outputs the bag of words and all samples as requested by assignment

	Args:
		bag - bag of words the headline file
		X_train - sentence samples for training
		y_train - sentence labels for training
		X_test - sentence samples for testing
		y_test - sentence labels for testing

	Returns:
		(none)
	"""
	with open(FILE_DIR + PP_TRAIN_FNAME, "w") as f:

		for word in bag:

			f.write("{},".format(word))

		f.write("classlabel\n")

		for i in range(len(X_train)):

			for val in X_train[i]:

				f.write("{},".format(val))

			f.write("{}\n".format(y_train[i]))

def train(bag, X_train, y_train):
	"""Trains a naive Bayes classifier on the bag of words given

	Args:
		bag - bag of words as a list
		X_train - feature vector of word frequency in sentences
		y_train - label vector of positive or negative review

	Returns:
		NaiveBayesClassifier object with weights gathered from X_train
	"""
	# Initialize classifier
	clf = nb.NaiveBayesClassifier(2, len(X_train[0]))

	# Add log priors
	clf.priors.append(np.log((len(y_train) - sum(y_train))/len(y_train)))
	clf.priors.append(np.log((sum(y_train))/len(y_train)))
	
	# Update word frequencies
	for i in range(len(X_train)):

		clf.frequency_list[y_train[i]] = np.add(X_train[i], 
			clf.frequency_list[y_train[i]])

	return clf

def test(clf, X_test, y_test):
	"""Tests a naive Bayes classifier on vectorized sentences

	Args:
		clf - trained naive bayes classifier object
		X_test - feature vector of word frequency in sentences
		y_train - label vector of positive or negative review

	Returns:
		(none)
	"""
	pred = []
	for i in range(len(X_test)):

		likelihood = [clf.priors[0], clf.priors[1]]

		for j in range(len(X_test[i])):

			# Find which words are in the "sentence"
			if X_test[i][j] == 1:

				likelihood[0] += np.log(
					clf.frequency_list[0][j] / sum(clf.frequency_list[0]))
				likelihood[1] += np.log(
					clf.frequency_list[1][j] / sum(clf.frequency_list[1]))

		pred.append(0) if likelihood[0] > likelihood[1] else pred.append(1)

	# Determine accuracy
	res = 0
	for i in range(len(pred)):

		res += 1 if pred[i] == y_test[i] else 0

	return res/len(pred)

def summary(training_results, testing_results):
	"""Writes a summary of NB classifier performance

	Args:
		training_results - accuracy of training
		testing_results - accuracy of testing

	Returns:
		(none)
	"""
	with open(FILE_DIR + RESULTS_FNAME, "w") as f:

		f.write("Training accuracy:\t{}\tTraining file: {}, Testing file: {}\n".format(training_results,
			TRAINING_FNAME, TRAINING_FNAME))
		f.write("Testing accuracy:\t{}\tTraining file: {}, Testing file: {}\n".format(testing_results,
			TRAINING_FNAME, TESTING_FNAME))

if __name__ == '__main__':
	main()