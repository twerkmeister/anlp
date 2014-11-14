import numpy as np
from collections import defaultdict,deque
import operator
from nltk.probability import FreqDist, SimpleGoodTuringProbDist
from math import log
from itertools import combinations

class HMM(object):

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

  def getLogEmissionProbability(self, state, word):
    return log(self.getEmissionProbability(state,word))

  def getLogTransitionProbability(self, *states):
    return log(self.getTransitionProbability(*states))

  def getEmissionProbability(self, state, word):
    return self.emission_probabilities[state][word]
  
  def getTransitionProbability(self, *states):
    return self.transition_probabilities[states]

  def calculateTransitionProbabilities(self):
    return self.transition_counts.astype("double") / self.transition_counts.sum()

  def calculateEmissionProbabilities(self):
    sums = [sum(d.values()) for d in self.emission_counts]
    return [defaultdict(int, {k:float(v)/sums[i] for k,v in d.items()}) for i,d in enumerate(self.emission_counts)]

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

  def __prob(self, trellis, t, state, word, past_states):
    if t==0:
      return (self.getLogTransitionProbability(*past_states + [state]) +  
             self.getLogEmissionProbability(state, word))
    else:
      return (trellis[t-1,past_states[-1]] + 
             self.getLogTransitionProbability(*past_states + [state]) +
             self.getLogEmissionProbability(state,word))

  def __viterbi(self, trellis, t, state, word):
    if t==0:
      return (len(self.stateNumbers), self.__prob(trellis, t, state, word, [len(self.states)]))
    else:
      results = []
      for past_state in self.stateNumbers:
        results.append(self.__prob(trellis, t, state, word, [past_state]))

      return max(enumerate(results), key=operator.itemgetter(1))

  def buildSequence(self, tags, pointers, t):
    if t <= 1:
      tags.reverse()
      return tags
    else:
      tags.append(pointers[t-1, tags[-1]])
      return self.buildSequence(tags, pointers, t-1)

  def tagSentence(self, sentence):
    # print "tagging %s" % " ".join(sentence)
    trellis = np.zeros((len(sentence), len(self.states)))
    pointers = trellis.copy()
    for t,word in enumerate(sentence):
      for state in self.stateNumbers:
        pointers[t,state], trellis[t,state] = self.__viterbi(trellis, t, state, word)
      
    final_tag, max_value = max(enumerate(trellis[t,]), key=operator.itemgetter(1))
    return self.buildSequence([final_tag], pointers, t)

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
    return SimpleGoodTuringProbDist(fd)

  def calculateEmissionProbabilities(self):
    return [self.createProbDist(d) for d in self.emission_counts]

  def getEmissionProbability(self, state, word):
    return self.emission_probabilities[state].prob(word)

class AddOneHMM(HMM):
  def calculateTransitionProbabilities(self):
    return self.transition_counts.astype("double") + 1 / (self.transition_counts.sum()+len(self.states)**self.n)

  def calculateEmissionProbabilities(self):
    sums = [sum(d.values()) for d in self.emission_counts]
    return [defaultdict(lambda: 1.0/len(d), {k:float(v)+1/(sums[i]+len(d)) for k,v in d.items()}) for i,d in enumerate(self.emission_counts)]

class FasterHMM(AddOneHMM):
  def calculateTransitionProbabilities(self):
    return np.log(super(AddOneHMM, self).calculateTransitionProbabilities())

  def getLogTransitionProbability(self, *states):
    return self.getTransitionProbability(*states)

  def calculateEmissionProbabilities(self):
    sums = [sum(d.values()) for d in self.emission_counts]
    return [defaultdict(lambda: log(1.0/len(d)), {k:log(float(v)+1/(sums[i]+len(d))) for k,v in d.items()}) for i,d in enumerate(self.emission_counts)]

  def getLogEmissionProbability(self, state, word):
    return self.getEmissionProbability(state,word)
