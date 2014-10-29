import nltk
from nltk.model.ngram import NgramModel

text = "This is a test. Feel free to check it out. This is a test. Check it out"

tokens = nltk.word_tokenize(text)

bigrams = NgramModel(2, tokens)



