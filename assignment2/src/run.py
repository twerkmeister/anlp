
from reader import TagReader
from hmm import HMM, SmoothedHMM
import sys
import codecs

UTF8Writer = codecs.getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)

tags = [u'ADV', u'NOUN', u'ADP', u'PRT', u'DET', u'.', u'PRON', u'VERB', u'X', u'NUM', u'CONJ', u'ADJ']

if __name__ == "__main__":
  tr = TagReader("../assets/de-train.tt", tags)
  observations = tr.readLines()
  hmm = SmoothedHMM(tags, observations, 3)
  # print(hmm)
  # words = ["Der", "Hauptgang", "war", "in", "Ordnung", ",", "aber", "alles", "andere", "als", "umwerfend"]
  words = ["Eine", "kleine", "Maus", "wohnt", "in", "unserem", "Haus"]
  tagged = tr.tag_transformer.transformAllToTags(hmm.tag(words))
  for word,tag in zip(words, tagged):
    print word, tag
