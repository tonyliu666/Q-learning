# valueIterationAgents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


import mdp, util
import pdb

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates() Ex: ['TERMINAL_STATE', (0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2), (3, 0), (3, 1), (3, 2)]
              mdp.getPossibleActions(state) Ex: ('north', 'west', 'south', 'east')
              mdp.getTransitionStatesAndProbs(state, action) Given the state and action, get the probabilities of next possible states, Ex: [((1, 2), 0.2), ((2, 2), 0.8)]
              mdp.getReward(state, action, nextState) Get the reward of the state
              mdp.isTerminal(state) Check if the state is terminal
        """
        self.mdp = mdp
        self.discount = discount # discount rate
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0

        # Write value iteration code here
        "*** YOUR CODE HERE ***"

        copy=util.Counter()
        for i in range(self.iterations):
          copy=self.values.copy()
          for state in self.mdp.getStates():
            print state
            all_actions=self.mdp.getPossibleActions(state)
            transitions=[]
            UtilityList=[]
            

            if self.mdp.isTerminal(state):
              self.values[state]=0
            else:
              for action in all_actions:
                transitions=self.mdp.getTransitionStatesAndProbs(state,action)
                print transitions
                # transitions=dict(transitions)
                value=0
                # for transition in transitions.items():
                for transition in transitions:
                  # value += transition[1]*(self.mdp.getReward(state, action, transition[0]) + self.discount * copy[transition[0]])
                  value += transition[1]*(self.mdp.getReward(state, action, transition[0]) + self.discount * copy[transition[0]])
                # for i in transitions.keys():
                #   transitions[i]=value

                # transitions[transition]=value
                UtilityList.append(value)
              self.values[state]=max(UtilityList)
              # self.values[state]=max(transitions.values())


        


    def getValue(self, state): #utility
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        
        value=0
        transitions=self.mdp.getTransitionStatesAndProbs(state, action)
        transitions=dict(transitions)
        for transition in transitions.items():
          value += transition[1]*(self.mdp.getReward(state, action, transition[0]) + self.discount * self.values[transition[0]])
        return value
        # util.raiseNotDefined()

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        if self.mdp.isTerminal(state):
          return None
        else:
          bestval=float("-Inf")
          bestaction=" "
          all_actions=self.mdp.getPossibleActions(state)
          for action in all_actions:
            transitions=self.mdp.getTransitionStatesAndProbs(state, action)
            value=0
            for transition in transitions:
              value += transition[1]*(self.mdp.getReward(state, action, transition[0]) + self.discount * self.values[transition[0]])
            if value > bestval:
              bestaction = action
              bestval = value
        return bestaction
        
    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
