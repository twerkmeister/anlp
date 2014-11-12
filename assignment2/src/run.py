
from reader import TagReader
from hmm import HMM, SmoothedHMM
import sys
import codecs
import numpy as np

UTF8Writer = codecs.getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)

tags = [u'ADV', u'NOUN', u'ADP', u'PRT', u'DET', u'.', u'PRON', u'VERB', u'X', u'NUM', u'CONJ', u'ADJ']
trainingDataFile = "../assets/de-train.tt"
testDataFile = "../assets/de-eval.tt"

np.set_printoptions(suppress=True)

def prettyPrintConfusionMatrix(confusion_matrix):
  table_head = " "*5
  for tag in tags:
    table_head += "%4s " % tag
  print table_head

  for i,line in enumerate(confusion_matrix):
    line_string = "%4s " % tags[i]
    for element in line:
      line_string += "%4d " % element
    line_string += "%5d" % line.sum()
    print line_string

  table_footer = " " * 5
  for row in confusion_matrix.transpose():
    table_footer += "%4d " % row.sum()
  print table_footer

if __name__ == "__main__":
  training = TagReader(trainingDataFile, tags)
  training_sentences = training.readSentences()
  test = TagReader(testDataFile, tags)
  test_sentences = test.readSentences()
  hmm = SmoothedHMM(tags, training_sentences, 3)
  # print(hmm)
  # words = ["Der", "Hauptgang", "war", "in", "Ordnung", ",", "aber", "alles", "andere", "als", "umwerfend"]
  confusion = hmm.test(test_sentences)
  prettyPrintConfusionMatrix(confusion)
