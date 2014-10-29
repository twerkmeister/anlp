import nltk
import os
import sys
from collections import Counter
from nltk.model.ngram import NgramModel

def read_and_tokenize(filename):
  f = file(filename, "r")
  text = f.read()
  tokenized = nltk.word_tokenize(text)
  tokenized = filter(lambda word: word.isalpha, tokenized)
  f.close()
  return tokenized

def pmi(w1,w2, bigrams, unigrams):
  return bigrams.prob(w2, [w1]) / (unigrams.prob(w1, []) * unigrams.prob(w2, []))


if __name__ == "__main__":
  os.chdir(os.path.dirname(sys.argv[0]) + "/../assets")
  filename = "AV1611Bible.txt"
  tokens = read_and_tokenize(filename)
  counts = Counter(tokens)
  frequent_words = [k for (k,v) in counts.items() if v >= 10]
  filtered_tokens = filter(lambda token: token in frequent_words, tokens)
  bigrams = NgramModel(2, filtered_tokens)
  unigrams = bigrams._backoff
  pmi_results = {}

  for i in range(len(filtered_tokens)-1):
    w1 = filtered_tokens[i]
    w2 = filtered_tokens[i+1]
    pmi_results[(w1, w2)] = pmi(w1, w2, bigrams, unigrams)

  pmi_sorted = sorted(pmi_results.items(), key=lambda (k,v): v)
  top20 = pmi_sorted[0:20]
  bottom20 = pmi_sorted[-20:]
  print(top20)
  print(bottom20)


