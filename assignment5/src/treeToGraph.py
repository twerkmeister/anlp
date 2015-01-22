
import copy
from graph import Node

class AbstractTreeToGraphAlgorithm(object):
  def __init__(self):
    pass

  def transform(self, tree):
    tree = copy.deepcopy(tree)
    return tree

  def addRootNode(self, graph):
    graph.add_complex_node(Node.rootNode())
    return graph

class BaselineTreeToGraphAlgorithm(AbstractTreeToGraphAlgorithm):
  def transform(self, tree):
    tree = copy.deepcopy(tree)
    tree = self.removeRootNode(tree)
    tree = self.removeNullEdges(tree)
    return tree

  def removeRootNode(self, tree):
    tree.remove_node(0)
    return tree

  def removeNullEdges(self, tree):
    for source, destinations in tree.edge.items():
      for dest, attr in destinations.items():
        if attr['label'] == "_null_":
          tree.remove_edge(source, dest)
    return tree





