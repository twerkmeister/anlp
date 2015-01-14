from graphreader import GraphReader
from graph import *
import sys


def main():
  graphReader = GraphReader(sys.argv[1])
  graphs = graphReader.readGraphs()
  for sentenceId, graph in graphs.items()[:2]:
    print sentenceId
    transformToGraph(graph)
  trees = None # transform graphs to trees
  back_transformed_graphs = None #transform those dependencies trees back


if __name__ == '__main__':
  if len(sys.argv) < 2:
    print "Usage:", sys.argv[0], "<treefilebank>"
  else:
    main()