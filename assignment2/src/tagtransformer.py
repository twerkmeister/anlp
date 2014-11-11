
class TagTransformer:
  def __init__(self, tags):
    self.tags = tags
    self.transformer = {tag:index for (index, tag) in enumerate(tags)}

  def transformToIndex(self, tag):
    return self.transformer[tag]

  def transformToTag(self, index):
    return self.tags[index]

  def transformAllToIndices(self, tags):
    for tag in tags:
      yield transformToIndex(tag)

  def transformAllToTags(self, indices):
    for index in indices:
      yield transformToTag(index)