import logging
from .CustomList import CustomList
from .State import State
from .Transition import Transition

class Automata:
    """Automata: is a self-operating machine, or a machine or control mechanism
    designed to automatically follow a predetermined sequence of operations, or
    respond to predetermined instructions
    """
    def __init__(self):
        self.logger = logging.getLogger('Automata')
        self.alphabet = None
        self.states = None
        self.transitions = None

    def __str__(self):
        alphabet = "Alphabet:\t{0}\n".format(self.alphabet)
        states = str(self.states)
        transitions = str(self.transitions)

        return alphabet+states+transitions

    def setAlphabet(self, alphabet):
        if( isinstance(alphabet, CustomList) ):
            self.alphabet = alphabet
        else:
            raise TypeError(alphabet)

    def getAlphabet(self):
        return self.alphabet

    def setStates(self, state):
        if( isinstance(state, CustomList) ):
            self.states = state
        else:
            raise TypeError(state)

    def getStates(self):
        return self.states

    def setTransition(self, transition):
        if( isinstance(transition, Transition) ):
            self.transitions = transition
        else:
            raise TypeError(transition)

    def getTransition(self):
        return self.transitions

    def isValidTransition(self, from_state, with_letter, to_state):
        is_valid = True
        if( from_state not in self.states ):
            is_valid = False
        elif( with_letter not in self.alphabet ):
            is_valid = False
        elif( to_state not in self.states ):
            is_valid = False

        return is_valid

    def evaluate(self, string):
        self.logger.debug("Evaluating string: {0}".format(string))
        result = True
        state = self.states.getStart()[0]
        for string_index, char in enumerate(string):
            self.logger.debug("Current State: {0}".format(state))
            self.logger.debug("Letter: {0}".format(char))
            try:
                letter_index = self.alphabet.index( char )
                state_index = self.states.index( state )
                next_state = self.transitions[state_index][letter_index]
                self.logger.debug("Next State: {0}".format(next_state))
                if( next_state is None ):
                    break
                else:
                    state = next_state
            except ValueError:
                break

        if(string_index != len(string)-1):
            result = False
        elif(next_state is None):
            result = False
        elif( state not in self.states.getFinal() ):
            result = False

        return result
