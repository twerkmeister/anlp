import numpy as np

class EMAlignment(object):
  
  def __init__(self, foreign_words, english_words):
    self.trans_prob = np.zeros((len(foreign_words), len(english_words)))
    self.trans_prob.fill(1.0 / len(english_words))
    self.foreign_index = {word:index for index,word in enumerate(foreign_words)}
    self.english_index = {word:index for index,word in enumerate(english_words)}
    self.initCounts()

  def t(self, f, e):
    return self.trans_prob[self.foreign_index[f], self.english_index[e]]

  def increaseCount(self, f, e, by):
    self.counts[self.foreign_index[f], self.english_index[e]] += by

  
  def initCounts(self):
    self.counts = np.zeros(self.trans_prob.shape)

  
  def normalizeCounts(self):
    for row in range(len(self.counts)):
      self.counts[row] = self.counts[row]/self.counts[row].sum() if self.counts[row].sum() > 0 else self.counts[row]
    # self.counts = np.apply_along_axis(lambda x: x/x.sum() if x.sum() > 0 else x, 1, self.counts)

  def adjustParameters(self):
    self.trans_prob = self.counts
    self.initCounts()


