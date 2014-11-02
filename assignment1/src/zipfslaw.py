import nltk
import os
import sys
import numpy
from collections import Counter
import matplotlib
import matplotlib.pyplot as plt
import io
import codecs

UTF8Writer = codecs.getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)

def read_and_tokenize(filename):
  with io.open(filename, "rt", encoding="utf-8") as f:
    text = f.read()
    tokenized = nltk.word_tokenize(text)
    tokenized = filter(lambda word: word.isalpha(), tokenized)
    tokenized = map(lambda word: word.lower(), tokenized)
    return tokenized

if __name__ == "__main__":
  script_dir = "." if os.path.dirname(sys.argv[0]) == "" else os.path.dirname(sys.argv[0])
  os.chdir(script_dir + "/../assets")
  #do for all
  for filename in filter(lambda filename: not filename.endswith(".png"), os.listdir(".")):
    print "processing %s" % filename
    tokens = read_and_tokenize(filename)
    counts = Counter(tokens)
    counts_only = counts.values()
    counts_only.sort(reverse=True)

    figure = plt.figure()
    #taking only the first 100 words for the linear plot
    figure.add_subplot(121).plot(counts_only[0:100])
    plt.title("%s linear" % filename)
    figure.add_subplot(122, aspect="equal").loglog(counts_only)
    plt.title("%s loglog" % filename)
    plt.savefig(filename+".png")
    
    c = []
    i = 1
    for word,count in counts.most_common(len(counts)):
      frequency_rank = float(count)/len(tokens) * i
      c.append(frequency_rank)
      i+=1
      if i < 20:
        print "%s:%d -> %.3f" % (word, count, frequency_rank)
    average_c = sum(c)/len(c)
    print "average c: %.3f" % average_c
    print ""



