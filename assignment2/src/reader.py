import io
from tagtransformer import TagTransformer

class TagReader:
  def __init__(self, filename, tags):
    self.f = io.open(filename, "rt", encoding="utf-8")
    self.tag_transformer = TagTransformer(tags)

  def __del__(self):
    self.f.close()

  def __readLines(self):
    buff = [1]
    while len(buff) > 0:
      buff = self.f.readlines(8096)
      yield buff

  def readLines(self):
    for buff in self.__readLines():
      for line in buff:
        if len(line) > 1:
          yield self.parseLine(line)

  def parseLine(self, line):
    word,tag = line.strip().split("\t")
    return(self.__transformWord(word), self.__transformTag(tag))

  def __transformTag(self, tag):
    return self.tag_transformer.transformToIndex(tag)

  def __transformWord(self, word):
    return word





