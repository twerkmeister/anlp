import sys
import io
import random
import os

if len(sys.argv) < 3:
  print "Usage: <#iterations> <testcase [1,2,3,all]>"
  sys.exit()


rounds = int(sys.argv[1])
testcase = sys.argv[2]
fileA = io.open("results/%s.berkeley" % testcase, "r")
fileB = io.open("results/%s.stanford" % testcase, "r")
observedA = fileA.readlines()
observedB = fileB.readlines()
fileA.close()
fileB.close()

def randomize(zippedAB):
  return map(lambda (a,b): (a,b) if random.random() > 0.5 else (b,a), zippedAB)

def createRandomizations():
  zippedAB = zip(observedA, observedB)
  folder = "results/testcase%s" % testcase
  if not os.path.exists(folder):
    os.mkdir(folder)
  for i in range(rounds):
    randomizedObservations = randomize(zippedAB)
    randomA, randomB = zip(*randomizedObservations)
    fileNameA = folder + "/roundA%.04d" % i
    fileNameB = folder + "/roundB%.04d" % i
    writeToFile(randomA, fileNameA)
    writeToFile(randomB, fileNameB) 

def writeToFile(randomizedObservations, fileName):
  with io.open(fileName, "w") as f:
    f.writelines(randomizedObservations)

createRandomizations()