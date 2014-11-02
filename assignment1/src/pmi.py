import nltk
import os
import sys
from collections import Counter
from nltk.model.ngram import NgramModel

def read_and_tokenize(filename):
  f = file(filename, "r")
  text = f.read()
  tokenized = nltk.word_tokenize(text)
  tokenized = filter(lambda word: word != "[" and word != "]" , tokenized)
  f.close()
  return tokenized

def pmi(w1,w2, bigrams, unigrams):
  return bigrams.prob(w2, [w1]) / (unigrams.prob(w1, []) * unigrams.prob(w2, []))

def printPMI(pmi_list):
  for bigram,pmi in pmi_list:
    print("%s %s -> %f" % (bigram[0], bigram[1], pmi))

if __name__ == "__main__":
  script_dir = "." if os.path.dirname(sys.argv[0]) == "" else os.path.dirname(sys.argv[0])
  os.chdir(script_dir + "/../assets")
  filename = "AV1611Bible.txt"
  tokens = read_and_tokenize(filename)
  counts = Counter(tokens)
  common_words = [k for (k,v) in counts.items() if v >= 10]
  # filtered_tokens = filter(lambda token: token in frequent_words, tokens)
  bigrams = NgramModel(2, tokens)
  unigrams = bigrams._backoff
  pmi_results = {}

  for i in range(len(tokens)-1):
    w1 = tokens[i]
    w2 = tokens[i+1]
    if w1 in common_words and w2 in common_words:
      pmi_results[(w1, w2)] = pmi(w1, w2, bigrams, unigrams)

  pmi_sorted = sorted(pmi_results.items(), key=lambda (k,v): v, reverse=True)
  top20 = pmi_sorted[0:20]
  bottom20 = pmi_sorted[-20:]
  print("Top 20 Pointwise mutual information:")
  print("====================================")
  printPMI(top20)
  print("Bottom 20 Pointwise mutual information:")
  print("=======================================")
  printPMI(bottom20)


