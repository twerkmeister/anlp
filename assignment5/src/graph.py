import networkx as nx
import matplotlib.pyplot as plt

class Node(object):
  def __init__(self, ID, word, lemma, POStag, isTopWord, isPredicate, *incomingEdges):
    self.ID = ID
    self.word = word
    self.lemma = lemma
    self.POStag = POStag
    self.isTopWord = True if isTopWord == "+" else False
    self.isPredicate = True if isPredicate == "+" else False
    self.incomingEdges = incomingEdges

def createDepdencyTreeFromGraph(graph):
  return graph

def createGraphFromDepdendencyTree(tree):
  return tree

class SemanticGraph(nx.DiGraph):
  def __init__(self, sentenceId, nodes):
    super(SemanticGraph, self).__init__()
    self.sentenceId = sentenceId
    self.initWithNodeList(nodes)

  def initWithNodeList(self, nodes):
    predicates = []
    for node in nodes:
      self.add_node(node.ID, node.__dict__)
      if node.isPredicate:
        predicates.append(node.ID)
    for node in nodes:
      for index,edge_label in enumerate(node.incomingEdges):
        if edge_label != "_":
          self.add_edge(predicates[index],node.ID,label = edge_label)

  def draw(self):
    nx.draw_networkx(self)
    plt.draw()
    plt.show()

  def stringify(self):
    def transformBoolean(b):
      if b: return "+"
      else: return "-"

    result = u"%s\n" % self.sentenceId
    for i in range(1, len(self.node)+1):
      node = self.node[str(i)]
      values = [node["ID"], node["word"], node["lemma"], node["POStag"], transformBoolean(node["isTopWord"]), transformBoolean(node["isPredicate"])]
      values += node["incomingEdges"]
      result += u"\t".join(values) + u"\n"
    return result