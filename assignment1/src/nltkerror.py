import nltk
from nltk.model.ngram import NgramModel

text = "This is a test. Feel free to check it out. This is a test. Check it out. This is a test. Check"

tokens = nltk.word_tokenize(text)

bigrams = NgramModel(2, tokens)

print("Seen words after \"test.\":")
bigrams[["test."]].freqdist().tabulate()

print("probablility to see \"Feel\" after \"test.\":")
print(bigrams[["test."]].prob("Feel")) # 0.266666666667
print(bigrams["test."].prob("Feel")) # 1.0
print(bigrams[["test."]].prob("Check")) # 0.4
print(bigrams["test."].prob("Check")) # 1.0

print(bigrams["is"].prob("a")) # 1.0
print(bigrams[["is"]].prob("a")) # 1.0

