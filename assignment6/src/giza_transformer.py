import sys
import re

alignment_regex = re.compile("\(\{(.*?)\}\)")
alignment_clean_regex = re.compile("(\(\{.*?\}\))")

def cleanSourceSentence(s):
  alignment_info = alignment_clean_regex.findall(s)
  for a in alignment_info:
    s = s.replace(a, "")
  return s.strip().split(" ")

def extractAlignment(s):
  alignments = alignment_regex.findall(s)
  alignments = map(lambda a: a.strip().split(" "), alignments)
  return alignments

if len(sys.argv) < 2:
  print "Usage %s <giza alignment file>" % sys.argv[0]
  sys.exit(1)

with open(sys.argv[1]) as f:
  lines = filter(lambda l: not l.startswith("#"), f.readlines())
  target = [line.strip().split(" ") for line in lines[0:len(lines):2]]
  (source,alignments) = zip(*[(cleanSourceSentence(line), extractAlignment(line)) for line in lines[1:len(lines):2]])

  for (t_s, s_s, a_s) in zip(target, source, alignments):
    for t_i, t in enumerate(t_s):
      for a_i, a in enumerate(a_s):
        if str(t_i+1) in a:
          sys.stdout.write("%i-%i " % (a_i-1,t_i))
    sys.stdout.write("\n")

