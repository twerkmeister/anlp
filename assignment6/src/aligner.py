#!/usr/bin/env python
import optparse
import sys
from collections import defaultdict
from translationmatrix import *

optparser = optparse.OptionParser()
optparser.add_option("-d", "--data", dest="train", default="../data/hansards", help="Data filename prefix (default=data)")
optparser.add_option("-e", "--english", dest="english", default="e", help="Suffix of English filename (default=e)")
optparser.add_option("-f", "--french", dest="french", default="f", help="Suffix of French filename (default=f)")
optparser.add_option("-t", "--threshold", dest="threshold", default=0.5, type="float", help="Threshold for aligning with Dice's coefficient (default=0.5)")
optparser.add_option("-n", "--num_sentences", dest="num_sents", default=sys.maxint, type="int", help="Number of sentences to use for training and alignment")
optparser.add_option("-r","--num_rounds", dest="num_rounds", default=100, type="int", help="Number of rounds to use for training the em model")

(opts, _) = optparser.parse_args()
f_data = "%s.%s" % (opts.train, opts.french)
e_data = "%s.%s" % (opts.train, opts.english)

sys.stderr.write("Training IBM Model I...\n")
bitext = [[sentence.strip().split() for sentence in pair] for pair in zip(open(f_data), open(e_data))[:opts.num_sents]]
foreign_words = set()
english_words = set()
for (f,e) in bitext:
  for f_i in f:
    foreign_words.add(f_i)
  for e_i in e:
    english_words.add(e_i)

EM = EMAlignment(foreign_words, english_words)

del(foreign_words)
del(english_words)

for i in range(0, opts.num_rounds):
  sys.stderr.write("EM training round %d\n" % i)
  for (f_s,e_s) in bitext:
    total_s = 0 
    for e in e_s:
      for f in f_s:
        total_s += EM.trans_prob[EM.foreign_index[f],EM.english_index[e]]
    for e in e_s:
      for f in f_s:
        EM.counts[EM.foreign_index[f], EM.english_index[e]] += EM.trans_prob[EM.foreign_index[f],EM.english_index[e]] / total_s
  EM.normalizeCounts()
  EM.adjustParameters()


for (f_s, e_s) in bitext:
  for e_i,e in enumerate(e_s):
    (f_i,f) = max(enumerate(f_s), key=(lambda (f_i, f): EM.t(f,e)))
    sys.stdout.write("%i-%i " % (f_i,e_i))
  sys.stdout.write("\n")



# f_count = defaultdict(int)
# e_count = defaultdict(int)
# fe_count = defaultdict(int)
# for (n, (f, e)) in enumerate(bitext):
#   for f_i in set(f):
#     f_count[f_i] += 1
#     for e_j in set(e):
#       fe_count[(f_i,e_j)] += 1
#   for e_j in set(e):
#     e_count[e_j] += 1
#   if n % 500 == 0:
#     sys.stderr.write(".")

# dice = defaultdict(int)
# for (k, (f_i, e_j)) in enumerate(fe_count.keys()):
#   dice[(f_i,e_j)] = 2.0 * fe_count[(f_i, e_j)] / (f_count[f_i] + e_count[e_j])
#   if k % 5000 == 0:
#     sys.stderr.write(".")
# sys.stderr.write("\n")

# for (f, e) in bitext:
#   for (i, f_i) in enumerate(f): 
#     for (j, e_j) in enumerate(e):
#       if dice[(f_i,e_j)] >= opts.threshold:
#         sys.stdout.write("%i-%i " % (i,j))
#   sys.stdout.write("\n")
