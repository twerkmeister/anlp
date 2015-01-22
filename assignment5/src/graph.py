import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict

class Node(object):
  def __init__(self, ID, word, lemma, POStag, isTopWord, isPredicate, *incomingEdges):
    self.ID = int(ID)
    self.word = word
    self.lemma = lemma
    self.POStag = POStag
    self.isTopWord = True if isTopWord == "+" else False
    self.isPredicate = True if isPredicate == "+" else False
    self.incomingEdges = incomingEdges

  @staticmethod
  def rootNode():
    return Node(u'0', u'__ROOT__', u'', u'', False, False, [])

def createGraphFromDepdendencyTree(tree):
  return tree

class SemanticGraph(nx.DiGraph):
  def __init__(self, sentenceId, nodes):
    super(SemanticGraph, self).__init__()
    self.sentenceId = sentenceId
    self.nodeList = nodes
    self.incomingEdges = {}
    self.predicates = []
    self.initWithNodeList(nodes)

  def add_complex_node(self, node):
    self.add_node(node.ID, node.__dict__)
    if node.isPredicate:
      self.predicates.append(node.ID)

  def initWithNodeList(self, nodes):
    for node in nodes:
      self.add_complex_node(node)
    for node in nodes:
      for index,edge_label in enumerate(node.incomingEdges):
        if edge_label != "_":
          self.add_edge(self.predicates[index],node.ID,label = edge_label)

  def add_node(self, *args, **kwargs):
    super(SemanticGraph, self).add_node(*args, **kwargs)
    self.updateIncomingEdges()

  def remove_node(self, *args, **kwargs):
    super(SemanticGraph, self).remove_node(*args, **kwargs)
    self.updateIncomingEdges()

  def add_edge(self, *args, **kwargs):
    super(SemanticGraph, self).add_edge(*args, **kwargs)
    self.updateIncomingEdges()

  def remove_edge(self, *args, **kwargs):
    super(SemanticGraph, self).remove_edge(*args, **kwargs)
    self.updateIncomingEdges()

  def updateIncomingEdges(self):
    self.incomingEdges = {node:{} for node in self.edge.keys()}
    for node,outgoingEdges in self.edge.items():
      for target,attr in outgoingEdges.items():
        self.incomingEdges[target][node]=attr

  def nodesWithoutIncomingEdges(self):
    return [ID for ID,sources in self.incomingEdges.items() if len(sources) == 0]

  def nodesWithoutOutgoingEdges(self):
    return [ID for ID,dest in self.edge.items() if len(dest) == 0]

  def singletons(self):
    nodesNoIncoming = self.nodesWithoutIncomingEdges()
    nodesNoOutgoing = self.nodesWithoutOutgoingEdges()
    singletons = [ID for ID in self.node.keys() if ID in nodesNoIncoming and ID in nodesNoOutgoing]
    return singletons

  def draw(self):
    labels = {ID:attr['word']+"("+str(ID)+")" for ID,attr in self.node.items()}
    nx.draw_networkx(self, labels=labels, node_color="w", node_size=1000, node_shape="_", font_size=15)
    plt.draw()
    plt.show()

  #I think this is only needed before writing to file
  def updateNodes(self):
    #find predicates
    self.predicates = []
    for source, destinations in self.edge.items():
      if len(destinations) > 0:
        self.predicates.append(source)
    self.predicates.sort()
    #update predicate status and incomingEdges list for nodes
    for ID, nodeAttr in self.node.items():
      nodeAttr["isPredicate"] = ID in self.predicates
      nodeAttr["incomingEdges"] = [u"_"] * len(self.predicates)
      for source,edgeAttr in self.incomingEdges[ID].items():
        predicateIndex = self.predicates.index(source)
        nodeAttr["incomingEdges"][predicateIndex] = edgeAttr["label"]

  def stringify(self):
    self.updateNodes()
    def transformBoolean(b):
      if b: return "+" 
      else: return "-"

    result = u"%s\n" % self.sentenceId
    for i in range(1, len(self.node)+1):
      node = self.node[i]
      values = [unicode(node["ID"]), node["word"], node["lemma"], node["POStag"], transformBoolean(node["isTopWord"]), transformBoolean(node["isPredicate"])]
      values += node["incomingEdges"]
      result += u"\t".join(values) + u"\n"
    return result