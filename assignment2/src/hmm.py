import numpy as np
from collections import defaultdict,deque
import operator
from nltk.probability import FreqDist, SimpleGoodTuringProbDist
from math import log
from itertools import product

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

  def getLogTransitionProbability(self, states):
    return log(self.getTransitionProbability(states))

  def getEmissionProbability(self, state, word):
    return self.emission_probabilities[state][word]
  
  def getTransitionProbability(self, states):
    return self.transition_probabilities[states]

  def calculateTransitionProbabilities(self):
    return self.transition_counts.astype("double") / self.transition_counts.sum()

  def calculateEmissionProbabilities(self):
    sums = [sum(d.values()) for d in self.emission_counts]
    return [defaultdict(int, {k:float(v)/sums[i] for k,v in d.items()}) for i,d in enumerate(self.emission_counts)]

  def attributeForEmission(self, state, word):
    self.emission_counts[state][word] += 1

  def attributeForTransition(self, states):
    self.transition_counts[states] += 1

  def train(self, annotated_sentences):
    for annotated_sentence in annotated_sentences:
      #start deque with beginning of sentence state
      state_window = deque([len(self.states)]*(self.n-1), maxlen=self.n)
      for word, state in annotated_sentence:
        self.attributeForEmission(state, word)
        state_window.append(state)
        #TODO:maybe the if can be taken out
        if(len(state_window) == self.n):
          self.attributeForTransition(tuple(state_window))

  def __prob(self, trellis, t, final_states, word, state):
    prior_log_prob = 0 if t == 0 else trellis[(t-1,) + (state,) + final_states[:-1]]
    transition_log_prob = self.getLogTransitionProbability((state,) + final_states)
    emission_log_prob = self.getLogEmissionProbability(final_states[-1],word)
    return prior_log_prob + transition_log_prob + emission_log_prob
             
  def __viterbi(self, trellis, t, final_states, word):
      results = []
      if(t < self.n -1):
        state = len(self.states)
        results = [(state, self.__prob(trellis, t, final_states, word, state))]
      else:
        results = [(state, self.__prob(trellis, t, final_states, word, state)) for state in self.stateNumbers]
      return max(results, key=operator.itemgetter(1))

  def buildSequence(self, tags, pointers, t):
    if t < self.n-1:
      return tags
    else:
      previous_tag = int(pointers[(t,) + tags[0:self.n-1]])
      return self.buildSequence((previous_tag,) + tags, pointers, t-1)

  def tagSentence(self, sentence):
    trellis = np.zeros((len(sentence),) + (len(self.states)+1,) * (self.n-1))
    pointers = trellis.copy()
    i = []
    for t,word in enumerate(sentence):
      start_states = (len(self.states),) * max(0, self.n - 2 - t)
      state_combos = [start_states + combo for combo in product(self.stateNumbers, repeat=min(self.n -1, t+1))]
      i.append(len(state_combos))
      for combo in state_combos:
        state, log_probability = self.__viterbi(trellis, t, combo, word)
        trellis_index = (t,) + combo
        trellis[trellis_index] = log_probability
        pointers[trellis_index] = state

      
    final_tags, max_value = max([(combo, trellis[(t,) + combo]) for combo in product(self.stateNumbers, repeat=self.n-1)], key=operator.itemgetter(1))
    return self.buildSequence(final_tags, pointers, t)

  def tagSentences(self, sentences):
    return [self.tagSentence(sentence) for sentence in sentences]

  def test(self, annotated_sentences, tag_writer = None):
    confusion_matrix = np.zeros((len(self.states), len(self.states)))
    for annotated_sentence in annotated_sentences:
      sentence,tags = zip(*annotated_sentence)
      inferred_tags = self.tagSentence(sentence)
      for tag,inferred_tag in zip(tags, inferred_tags):
        confusion_matrix[tag,inferred_tag] += 1
      if(tag_writer):
        tag_writer.writeSentence(sentence, inferred_tags)

    return confusion_matrix

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
    return (self.transition_counts.astype("double") + 1.0/self.n) / (self.transition_counts.sum()+len(self.states)**(self.n-1))

  def calculateEmissionProbabilities(self):
    sums = [sum(d.values()) for d in self.emission_counts]
    return [defaultdict(lambda: 1.0/len(d), {k:float(v)+1/(sums[i]+len(d)) for k,v in d.items()}) for i,d in enumerate(self.emission_counts)]