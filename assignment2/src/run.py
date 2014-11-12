
from reader import TagReader

tags = [u'ADV', u'NOUN', u'ADP', u'PRT', u'DET', u'.', u'PRON', u'VERB', u'X', u'NUM', u'CONJ', u'ADJ']

if __name__ == "__main__":
  tr = TagReader("../assets/de-train.tt", tags)
  for word,tag in tr.readLines():
    print word, tag
