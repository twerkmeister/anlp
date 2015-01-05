import sys
import os
import io
import re

if len(sys.argv) < 4:
  print "Usage: <testcase> <mode> <rounds>"
  sys.exit()

testcase = sys.argv[1]
mode = sys.argv[2]
rounds = int(sys.argv[3])

folder = "results/testcase%s" % testcase

recallPattern = re.compile("Bracketing Recall\s*=\s*([0-9]*\.[0-9]*)")
precisionPattern = re.compile("Bracketing Precision\s*=\s*([0-9]*\.[0-9]*)")
fmeasurePattern = re.compile("Bracketing FMeasure\s*=\s*([0-9]*\.[0-9]*)")

stanfordEval = io.open("results/%s.stanford.eval.%s" % (testcase, mode))
berkeleyEval = io.open("results/%s.berkeley.eval.%s" % (testcase, mode))

stanfordText = stanfordEval.read()
berkeleyText = berkeleyEval.read()
stanfordEval.close()
berkeleyEval.close()

stanfordRecall = float(recallPattern.search(stanfordText).group(1))
stanfordPrecision = float(precisionPattern.search(stanfordText).group(1))
stanfordFmeasure = float(fmeasurePattern.search(stanfordText).group(1))

berkeleyRecall = float(recallPattern.search(berkeleyText).group(1))
berkeleyPrecision = float(precisionPattern.search(berkeleyText).group(1))
berkeleyFmeasure = float(fmeasurePattern.search(berkeleyText).group(1))

recallDiff = abs(berkeleyRecall - stanfordRecall)
precisionDiff = abs(berkeleyPrecision - stanfordPrecision)
fmeasureDiff = abs(berkeleyFmeasure - stanfordFmeasure)

print "testcase %s %s" % (testcase, mode)
print "stanford Recall: %f" % stanfordRecall
print "stanford Precision: %f" % stanfordPrecision
print "stanford FMeasure: %f" % stanfordFmeasure
print "berkeley Recall: %f" % berkeleyRecall
print "berkeley Precision: %f" % berkeleyPrecision
print "berkeley FMeasure: %f" % berkeleyFmeasure
print "recall diff: %f " % recallDiff
print "precision diff: %f" % precisionDiff
print "fmeasure diff: %f" % fmeasureDiff

extractedRecall = []
extractedPrecision = []
extractedFmeasure = []

evaluations = [("roundA%.04d.eval.%s" % (r, mode), "roundB%.04d.eval.%s" % (r, mode)) for r in range(rounds)]

def extract(pattern, text):
  return float(pattern.search(text).group(1))

def extractRecall(text):
  return extract(recallPattern, text)

def extractPrecision(text):
  return extract(precisionPattern, text)

def extractFmeasure(text):
  return extract(fmeasurePattern, text)

for fileA,fileB in evaluations:
  a = io.open(folder+"/"+fileA)
  b = io.open(folder+"/"+fileB)
  textA = a.read()
  textB = b.read()
  extractedRecall.append(abs(extractRecall(textA) - extractRecall(textB)))
  extractedPrecision.append(abs(extractPrecision(textA) - extractPrecision(textB)))
  extractedFmeasure.append(abs(extractFmeasure(textA) - extractFmeasure(textB)))
  a.close()
  b.close()

recallCount = len(filter(lambda d: d >= recallDiff, extractedRecall))
precisionCount = len(filter(lambda d: d >= precisionDiff, extractedPrecision))
fmeasureCount = len(filter(lambda d: d >= fmeasureDiff, extractedFmeasure))

print "recall p: %f" % (float(recallCount) / rounds)
print "precision p: %f" % (float(precisionCount) / rounds)
print "fmeasure p: %f" % (float(fmeasureCount) / rounds)

