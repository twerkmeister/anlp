from collections import defaultdict

class EMAlignment(object):
  
  def __init__(self, foreign_words, english_words):
    self.t = defaultdict(lambda: defaultdict(lambda: 1.0/len(english_words)))
    self.initCounts()

  def initCounts(self):
    self.counts = defaultdict(lambda:defaultdict(int))
    self.total = defaultdict(int)

  def adjustParameters(self):
    self.t = self.counts
    self.initCounts()


