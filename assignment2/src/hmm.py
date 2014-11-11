import numpy as np
from collections import defaultdict

class HMM:

  def __init__(self, states, observedWords, observedStates, n = 2):
    self.states = states
    self.n = n
    self.transition_probabilities = self.initTransitionProbabilities(states, n)
    self.emission_probabilities = self.initEmissionProbabilities(states)
    observe(observedWords, observedStates)

  def initTransitionProbabilities(self, states, n):
    return np.zeros(len(states),) * n

  def initEmissionProbabilities(self, states, observedWords):
    return [defaultdict(int) for state in states]

  def getEmissionProbability(self, state, word):
    return self.emission_probabilities[state][word]
  
  def getTransitionProbability(self, *states):
    return self.transition_probabilities[states]

  def attributeForEmission(self, state, word):
    self.emission_probabilities[state][word] += 1

  def attributeForTransition(self, *states):
    self.transition_probabilities[states] += 1

  def observe(observedWords, observedStates):
    for word,state in zip(observedWords, observedStates):
      pass


