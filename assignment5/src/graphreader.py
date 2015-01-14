import io
from collections import defaultdict
from graph import Node

class GraphReader:
  def __init__(self, filename):
    self.filename = filename

  def readGraphs(self):
    f = io.open(self.filename)
    lines = f.readlines()
    graphs = defaultdict(list)
    sentenceId = ""
    for line in lines:
      if line.startswith("#"):
        sentenceId = line.strip()
      elif line.startswith("\n"):
        pass
      else:
        splitted = line.strip().split("\t")
        graphs[sentenceId].append(Node(*splitted))
    f.close()
    return graphs
