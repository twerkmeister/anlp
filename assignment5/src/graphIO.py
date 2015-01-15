import io
from collections import defaultdict
from graph import Node

class GraphReader:
  def __init__(self, filename):
    self.filename = filename

  def readNodeLists(self):
    f = io.open(self.filename, "rt", encoding="utf-8")
    lines = f.readlines()
    graphs = defaultdict(list)
    sentenceId = ""
    nodeLists = []
    for line in lines:
      if line.startswith("#"):
        sentenceId = line.strip()
        nodeLists.append((sentenceId, []))
      elif line.startswith("\n"):
        pass
      else:
        splitted = line.strip().split("\t")
        nodeLists[-1][1].append(Node(*splitted))
    f.close()
    return nodeLists

class GraphWriter:
  def __init__(self, filename):
    self.filename = filename

  def writeNodeLists(self, graphs):
    f = io.open(self.filename, "w", encoding="utf-8")
    for graph in graphs:
      f.write(graph.stringify())
      f.write(u"\n")
    f.close()