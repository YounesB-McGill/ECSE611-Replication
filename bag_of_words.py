from string import ascii_lowercase
from string import ascii_uppercase
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer


def intake_file(filename):
	file = open(filename, 'r')

	Lines = file.readlines()

	all_lines = []


	for line in Lines:
		line = line.strip()
		if len(line) == 0:
			continue
		if line[0] == '#':
			continue
		else:
			all_lines.append(line)
	return all_lines

def split_tokens(file):
	list_of_words = []
	counter = 0
	for line in file:
		current_word = ''
		for letter in line:
			if letter == ' ':
				if current_word != '':
					list_of_words.append(current_word)
					current_word = ''
			elif letter in ascii_lowercase:
				current_word = current_word + letter
			elif letter in ascii_uppercase:
				current_word = current_word + letter
			else:
				if current_word != '':
					list_of_words.append(current_word)
					current_word = ''
		if current_word != '':
			list_of_words.append(current_word)
	return list_of_words

def split_camel_case(words):
	new_words = []
	camel_words = []
	for word in words:
		camel_case = False
		current_word = ''
		for i in range(0, len(word)):
			if word[i] in ascii_uppercase:
				if i == len(word)-1:
					current_word = current_word + word[i]
				elif i == 0:
					current_word = current_word + word[i]
				elif (word[i-1] in ascii_lowercase) and (word[i+1] in ascii_lowercase):
					camel_case = True
					new_words.append(current_word)
					current_word = word[i]
			else:
				current_word = current_word+word[i]
		if camel_case == True:
			camel_words.append(word)
			new_words.append(current_word)
	for word in camel_words:
		words.remove(word)
	for word in new_words:
		words.append(word)
	return words

def preprocess_data(words):
	stop_words = stopwords.words('english')
	new_words = []
	final_words = []
	ps = PorterStemmer()
	for word in words:
		word = word.lower()
		if word not in stop_words:
			new_words.append(word)

	for word in new_words:
		final_words.append(ps.stem(word))
	return(final_words)

def create_bag_of_words(words):
	word_freq = {}
	for word in words:
		if word not in word_freq:
			word_freq[word] = 1
		else:
			word_freq[word] += 1
	return(word_freq)

def run_all_bag_of_words(filename):
	file_list = intake_file(filename)
	initial_tokens = split_tokens(file_list)
	new_words = split_camel_case(initial_tokens)
	final_words = preprocess_data(new_words)
	bag_of_words = create_bag_of_words(final_words)
	return bag_of_words

print(run_all_bag_of_words('git-repo/site.pp'))