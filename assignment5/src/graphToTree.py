import copy
from graph import Node

class AbstractGraphToTreeAlgorithm(object):
  def __init__(self):
    pass

  def transform(self, graph):
    graph = copy.deepcopy(graph)
    graph = self.eliminateReentrancies(graph)
    graph = self.addRootNode(graph)
    graph = self.attachSingletons(graph)
    return graph

  def eliminateReentrancies(self, graph):
    raise NotImplementedError("Abstract")

  def attachSingletons(self, graph):
    raise NotImplementedError("Abstract")

  def addRootNode(self, graph):
    graph.add_complex_node(Node.rootNode())
    return graph

class BaselineGraphToTreeAlgorithm(AbstractGraphToTreeAlgorithm):
  def eliminateReentrancies(self, graph):
    reEntrancingEdges = dict(filter(lambda (k,v): len(v) > 1, graph.incomingEdges.items()))
    for node, reEntrancingNodes in reEntrancingEdges.items():
      closest = None
      for reEntrancingNode, attr in reEntrancingNodes.items():
        if (closest == None or
           abs(node - reEntrancingNode) < abs(node - closest) or 
           (abs(node - reEntrancingNode) == abs(node - closest) and reEntrancingNode < closest)):
          if closest != None:
            graph.remove_edge(closest, node)
          closest = reEntrancingNode
        else:
          graph.remove_edge(reEntrancingNode, node)
    return graph

  def attachSingletons(self, graph):
    #attach last node to root
    finalNode = max(graph.node.keys())
    if finalNode in graph.singletons():
      graph.add_edge(0, finalNode, edge_label = "_null_")

    #attach all singletons to next node
    singletons = graph.singletons()
    singletons.sort()

    for singleton in singletons: 
      nextNode = singleton + 1
      if nextNode in graph.node.keys():
        graph.add_edge(nextNode, singleton, edge_label = "_null_")

    for node in graph.nodesWithoutIncomingEdges():
      graph.add_edge(0, node, edge_label = "_root_")
    
    import pdb; pdb.set_trace()
    

    #attach


    return graph




