import nltk
import os
import sys
import numpy
from collections import Counter
import matplotlib
import matplotlib.pyplot as plt


def read_and_tokenize(filename):
  f = file(filename, "r")
  text = f.read()
  tokenized = nltk.word_tokenize(text)
  tokenized = filter(lambda word: word.isalpha, tokenized)
  f.close()
  return tokenized

if __name__ == "__main__":
  os.chdir(os.path.dirname(sys.argv[0]) + "/../assets")
  #do for all
  for filename in os.listdir("."):
    tokens = read_and_tokenize(filename)
    counts = Counter(tokens)
    counts_only = counts.values()
    counts_only.sort(reverse=True)

    figure = plt.figure()
    figure.add_subplot(121).plot(counts_only[0:100])
    plt.title("%s linear" % filename)
    figure.add_subplot(122).loglog(counts_only[0:100])
    plt.title("%s loglog" % filename)
    plt.show()
  #draw counts



