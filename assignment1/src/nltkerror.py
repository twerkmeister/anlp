import nltk
from nltk.model.ngram import NgramModel

text = "This is a test. Feel free to check it out. This is a test. Check it out"

tokens = nltk.word_tokenize(text)

bigrams = NgramModel(2, tokens)

print("Seen words after \"test.\":")
bigrams[["test."]].freqdist().tabulate()

print("probablility to see \"Feel\" after \"test.\":")
print(bigrams[["test."]].prob("Feel"))

