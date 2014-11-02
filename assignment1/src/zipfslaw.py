import nltk
import os
import sys
import numpy
from collections import Counter
import matplotlib
import matplotlib.pyplot as plt
import io


def read_and_tokenize(filename):
  with io.open(filename, "rt", encoding="utf-8") as f:
    text = f.read()
    tokenized = nltk.word_tokenize(text)
    tokenized = filter(lambda word: word.isalpha(), tokenized)
    return tokenized

if __name__ == "__main__":
  script_dir = "." if os.path.dirname(sys.argv[0]) == "" else os.path.dirname(sys.argv[0])
  os.chdir(script_dir + "/../assets")
  #do for all
  for filename in filter(lambda filename: not filename.endswith(".png"), os.listdir(".")):
    tokens = read_and_tokenize(filename)
    counts = Counter(tokens)
    counts_only = counts.values()
    counts_only.sort(reverse=True)

    figure = plt.figure()
    #taking only the first 100 words for the linear plot
    figure.add_subplot(121).plot(counts_only[0:100])
    plt.title("%s linear" % filename)
    figure.add_subplot(122).loglog(counts_only)
    plt.title("%s loglog" % filename)
    plt.savefig(filename+".png")




