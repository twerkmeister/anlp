import io
from tagtransformer import TagTransformer

class TagWriter:
  def __init__(self, filename, tags):
    self.f = io.open(filename, "w", encoding="utf-8")
    self.tag_transformer = TagTransformer(tags)

  def __del__(self):
    self.f.close()

  def writeSentence(self, sentence, tags):
    for word,tag in zip(sentence, tags):
      real_tag = self.tag_transformer.transformToTag(int(tag))
      self.f.write(word + "\t" + real_tag + "\n")
    self.f.write(u"\n")





