import nltk
import os
import sys
from nltk.model.ngram import NgramModel
import random
import re

# Suppress those annoying error messages about the probability distributions
class DevNull:
    def write(self, msg):
        pass
sys.stderr = DevNull()

def read_and_tokenize(filename):
  f = file(filename, "r")
  text = f.read()
  tokenized = nltk.word_tokenize(text)
  tokenized = filter(lambda word: word != "[" and word != "]" , tokenized)
  f.close()
  return tokenized

def create_ngram_models(tokens):
  model = NgramModel(4, tokens)
  models = [model]
  for i in range(0, 3):
    models.append(models[-1]._backoff)
  models.reverse()
  return models

if __name__ == "__main__":
  script_dir = "." if os.path.dirname(sys.argv[0]) == "" else os.path.dirname(sys.argv[0])
  os.chdir(script_dir + "/../assets")
  for filename in os.listdir(".")[0:1]:
    tokens = read_and_tokenize(filename)
    models = create_ngram_models(tokens)

    for n in range(2,5):
      start = random.sample(tokens, n-1)
      generated = models[n-1].generate(100, context=start)
      # generated = start
      # for i in range(0,100):
      #   next_word = ""
      #   for backoff_n in range(n-1, -1, -1):
      #     if(backoff_n != n-1):
      #       print "backing of to %d" % backoff_n
      #     prob_dist = models[backoff_n][generated[-backoff_n:]]
      #     if len(prob_dist.samples()) > 0:
      #       next_word = prob_dist.generate()
      #       break
      #   generated.append(next_word)

      result = " ".join(generated)
      correct_punctuation = re.compile(" ([;,:.\'#?])")
      result = re.sub(correct_punctuation, lambda matchobj: matchobj.group(1), result)
      print("\n%d-grams:\n========" % n)
      print(result)

    