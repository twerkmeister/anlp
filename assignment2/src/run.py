
from reader import TagReader
from writer import TagWriter
from hmm import HMM, SmoothedHMM, AddOneHMM, FasterHMM
import sys
import codecs
import numpy as np

UTF8Writer = codecs.getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)

tags = [u'ADV', u'NOUN', u'ADP', u'PRT', u'DET', u'.', u'PRON', u'VERB', u'X', u'NUM', u'CONJ', u'ADJ']
trainingDataFile = "../assets/de-train.tt"
testDataFile = "../assets/de-eval.tt"
ResultsFile = "../assets/de-result.tt"

np.set_printoptions(suppress=True)

def prettyPrintConfusionMatrix(confusion_matrix):
  table_head = " "*5
  for tag in tags:
    table_head += "%4s " % tag
  table_head += "  sum " 
  table_head += "recall"
  print table_head
  recalls = []
  for i,row in enumerate(confusion_matrix):
    line_string = "%4s " % tags[i]
    for element in row:
      line_string += "%4d " % element
    line_string += "%5d " % row.sum()
    recalls.append(float(row[i]) / row.sum())
    line_string += "%.02f" % (recalls[-1])
    print line_string
  avg_recall = float(sum(recalls)) / len(recalls)
  total = 0
  table_footer = " sum "
  for col in confusion_matrix.transpose():
    total += col.sum()
    table_footer += "%4d " % col.sum()
  table_footer+="%5d " % total
  table_footer+="%.2f" % avg_recall
  table_footer+="\n"
  table_footer+= "prec "
  precisions = []
  total = 0
  for i,col in enumerate(confusion_matrix.transpose()):
    precision = float(col[i]) / col.sum()
    table_footer += "%.02f " % precision 
    precisions.append(precision)
  avg_precision = float(sum(precisions)) / len(precisions)
  table_footer += " %.02f " % avg_precision
  f1 = 2 * avg_precision * avg_recall / (avg_precision + avg_recall)
  table_footer += "%.02f (f1)" % f1
  print table_footer

if __name__ == "__main__":
  training = TagReader(trainingDataFile, tags)
  training_sentences = training.readSentences()
  test = TagReader(testDataFile, tags)
  test_sentences = test.readSentences()
  hmm = AddOneHMM(tags, training_sentences, 2)
  # print(hmm)
  # words = ["Der", "Hauptgang", "war", "in", "Ordnung", ",", "aber", "alles", "andere", "als", "umwerfend"]
  writer = TagWriter(ResultsFile, tags)
  confusion = hmm.test(test_sentences, writer)
  prettyPrintConfusionMatrix(confusion)
