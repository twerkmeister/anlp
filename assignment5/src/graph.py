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

def transformToGraph(nodes):
  G = nx.DiGraph()
  predicates = []
  for node in nodes:
    G.add_node(node.ID, node.__dict__)
    if node.isPredicate:
      predicates.append(node.ID)
  for node in nodes:
    for index,edge_label in enumerate(node.incomingEdges):
      if edge_label != "_":
        G.add_edge(predicates[index],node.ID,label = edge_label)

  import pdb; pdb.set_trace()
  nx.draw(G)
  plt.draw()
  plt.show()