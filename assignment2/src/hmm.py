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

  def __prob(self, trellis, t, state, word, past_states):
    if t==0:
      return (self.getLogTransitionProbability(past_states + (state,)) +  
             self.getLogEmissionProbability(state, word))
    else:
      return (trellis[(t-1,) + past_states] + 
             self.getLogTransitionProbability(past_states + (state,)) +
             self.getLogEmissionProbability(state,word))

  def __viterbi(self, trellis, t, state, word):
      start_states = (len(self.states),) * max(0, self.n - 1 - t)
      past_states_combos = [start_states + combo for combo in combinations(self.stateNumbers, min(self.n -1, t))]
      results = [(combo, self.__prob(trellis, t, state, word, combo)) for combo in past_states_combos ]
      # if self.first:
        # print results
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
    for t,word in enumerate(sentence):
      for state in self.stateNumbers:
        past_states, log_probability = self.__viterbi(trellis, t, state, word)
        fill_states = past_states[-(self.n-2):] if self.n > 2 else tuple()
        trellis_index = (t,) + fill_states + (state,)
        if(self.first)
          print trellis_index
        trellis[trellis_index] = log_probability
        pointers[trellis_index] = past_states[0]

    if(self.first):
      # print pointers
      # print trellis
      self.first = False
      
    final_tags, max_value = max([(combo, trellis[(t,) + combo]) for combo in combinations(self.stateNumbers, self.n-1)], key=operator.itemgetter(1))
    return self.buildSequence(final_tags, pointers, t)

  def tagSentences(self, sentences):
    return [self.tagSentence(sentence) for sentence in sentences]

  def test(self, annotated_sentences, tag_writer = None):
    self.first = True
    confusion_matrix = np.zeros((len(self.states), len(self.states)))
    print self.transition_probabilities[(12,12)]
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
    return (self.transition_counts.astype("double") + 1) / (self.transition_counts.sum()+len(self.states)**self.n)

  def calculateEmissionProbabilities(self):
    sums = [sum(d.values()) for d in self.emission_counts]
    return [defaultdict(lambda: 1.0/len(d), {k:float(v)+1/(sums[i]+len(d)) for k,v in d.items()}) for i,d in enumerate(self.emission_counts)]

class FasterHMM(AddOneHMM):
  def calculateTransitionProbabilities(self):
    return np.log(super(AddOneHMM, self).calculateTransitionProbabilities())

  def getLogTransitionProbability(self, states):
    return self.getTransitionProbability(states)

  def calculateEmissionProbabilities(self):
    sums = [sum(d.values()) for d in self.emission_counts]
    return [defaultdict(lambda: log(1.0/len(d)), {k:log(float(v)+1/(sums[i]+len(d))) for k,v in d.items()}) for i,d in enumerate(self.emission_counts)]

  def getLogEmissionProbability(self, state, word):
    return self.getEmissionProbability(state,word)
