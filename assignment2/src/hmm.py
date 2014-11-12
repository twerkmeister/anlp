import numpy as np
from collections import defaultdict,deque
import operator
import nltk
from nltk.probability import FreqDist, GoodTuringProbDist

class HMM:

  def __init__(self, states, sentences, n = 2):
    self.states = states
    self.stateNumbers = range(0, len(states))
    self.n = n
    self.transition_counts = self.initTransitionCounts(states, n)
    self.emission_counts = self.initEmissionCounts(states)
    self.train(sentences)
    self.emission_probabilities = self.calculateEmissionProbabilities()
    self.transition_probabilities = self.calculateTransitionProbabilities()

  def initTransitionCounts(self, states, n):
    #+1 for start of sentence state!
    return np.zeros((len(states)+1,) * n)

  def initEmissionCounts(self, states):
    return [defaultdict(int) for state in states]

  def getEmissionProbability(self, state, word):
    return self.emission_probabilities[state][word]
  
  def getTransitionProbability(self, *states):
    return self.transition_probabilities[states].sum()

  def calculateTransitionProbabilities(self):
    return self.transition_counts.astype("double") / self.transition_counts.sum()

  def calculateEmissionProbabilities(self):
    return [defaultdict(int, {k:float(v)/len(d) for k,v in d.items()}) for d in self.emission_counts]

  def attributeForEmission(self, state, word):
    self.emission_counts[state][word] += 1

  def attributeForTransition(self, *states):
    self.transition_counts[states] += 1

  def train(self, annotated_sentences):
    for annotated_sentence in annotated_sentences:
      #start deque with beginning of sentence state
      state_window = deque([len(self.states)], maxlen=self.n)
      for word, state in annotated_sentence:
        self.attributeForEmission(state, word)
        state_window.append(state)
        if(len(state_window) == self.n):
          self.attributeForTransition(*state_window)

  def tagSentence(self, sentence):
    trellis = np.zeros((len(sentence), len(self.states)))
    pointers = []
    #start deque with beginning of sentence state
    state_window = deque([len(self.states)], maxlen=self.n-1)
    for t,word in enumerate(sentence):
      for state in self.stateNumbers:
        trellis[t,state] = self.getEmissionProbability(state, word) * self.getTransitionProbability(*list(state_window) + [state])
        index, value = max(enumerate(trellis[t,]), key=operator.itemgetter(1))
      pointers.append(index)
      state_window.append(index)

    return pointers

  def tagSentences(self, sentences):
    return [self.tagSentence(sentence) for sentence in sentences]

  def test(self, annotated_sentences):
    confusion_matrix = np.zeros((len(self.states), len(self.states)))

    for annotated_sentence in annotated_sentences:
      sentence,tags = zip(*annotated_sentence)
      inferred_tags = self.tagSentence(sentence)
      for tag,inferred_tag in zip(tags, inferred_tags):
        confusion_matrix[tag,inferred_tag] += 1

    return confusion_matrix

  def __str__(self):
    res = "states: %s\n\n" % ", ".join(self.states)
    res += "transitions:\n"
    res += str(self.transition_probabilities)
    #res += "\n\n"
    #res += "emissions:\n"
    #res += str(self.emission_probabilities)
    return res

class SmoothedHMM(HMM):

  def createProbDist(self, counts):
    fd = FreqDist(counts)
    return GoodTuringProbDist(fd)

  def calculateEmissionProbabilities(self):
    return [self.createProbDist(d) for d in self.emission_counts]

  def getEmissionProbability(self, state, word):
    return self.emission_probabilities[state].prob(word)
