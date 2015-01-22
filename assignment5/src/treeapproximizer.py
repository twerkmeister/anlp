from graphIO import GraphReader, GraphWriter
from graph import *
from graphToTree import BaselineGraphToTreeAlgorithm
import sys

import codecs

UTF8Writer = codecs.getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)

def main():
  graphReader = GraphReader(sys.argv[1])
  graphToTreeTransformer = BaselineGraphToTreeAlgorithm()

  nodeLists = graphReader.readNodeLists()
  graphs = [SemanticGraph(sentenceId, nodes) for sentenceId, nodes in nodeLists]
  trees = [graphToTreeTransformer.transform(graph) for graph in graphs]
  import pdb; pdb.set_trace()
  back_transformed_graphs = [createGraphFromDepdendencyTree(tree) for tree in trees]
  graphWriter = GraphWriter(sys.argv[1]+".processed")
  graphWriter.writeNodeLists(graphs)

if __name__ == '__main__':
  if len(sys.argv) < 2:
    print "Usage:", sys.argv[0], "<treefilebank>"
  else:
    main()