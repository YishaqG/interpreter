import logging
from .CustomList import CustomList
from .State import State
from .Transition import Transition


KEYS = ['alphabet', 'states', 'transitions']
class Automata:
    """Automata: is a self-operating machine, or a machine or control mechanism
    designed to automatically follow a predetermined sequence of operations, or
    respond to predetermined instructions
    """

    def __init__(self):
        self.logger = logging.getLogger('Automata')
        self.alphabet = None
        self.states = None
        self.transitions = Transition()

    def __str__(self):
        alphabet = "Alphabet:\n{0}\n".format(self.alphabet)
        states = str(self.states)
        transitions = str(self.transitions)

        return alphabet+states+transitions

    def loadFromDict(self, data):
        self._validateDict(data)
        self.setAlphabet( data[KEYS[0]][0] )
        self.setStates( data )
        self.setTransitions( data[KEYS[2]] )
        print(self)

    def _validateDict(self, data):
        for key in KEYS:
            if( key not in data ):
                error_msg = "Unable to load <Automata> from %r" % data
                raise Error(error_msg)

    def setAlphabet(self, alphabet):
        if( isinstance(alphabet, CustomList) ):
            self.alphabet = alphabet
        elif( isinstance(alphabet, list) ):
            self.alphabet = CustomList(alphabet)
        else:
            raise TypeError(alphabet)

    def getAlphabet(self):
        return self.alphabet

    def setStates(self, data):
        self.states = State( data )
        self.states.loadStates( data )

    def getStates(self):
        return self.states

    def setTransitions(self, transitions_array):
        self.transitions.loadTransitions(
            transitions_array,
            self.alphabet,
            self.states
            )

    def getTransition(self):
        return self.transitions

    def restart(self):
        self.states.setCurrent( self.states.getStart()[0] )

    def evaluate(self, char):
        """Return the final state, None otherwise"""

        from_state = self.states.getCurrent()

        if(char is None): #To-Other
            return self.getOther(char, from_state)

        letter_index = self.alphabet.index( char )
        state_index = self.states.index( from_state )
        to_state = self.transitions[state_index][letter_index]

        if( to_state is None ):
            self.states.setCurrent( self.states.getStart()[0] )
            candidates = self.getCandidateCharacters(state_index)
            error_msg = BadSequenceException.buildMessage(char, from_state, candidates)
            raise BadSequenceException(error_msg)
        else:
            self.states.setCurrent( to_state )

        return self.states.isFinal( to_state )

    def getCandidateCharacters(self, from_state):
        # Returns the follwing valid characters
        candidates = []
        for index, transition in enumerate(self.transitions[from_state]):
            if(transition is not None):
                candidates.append( self.alphabet[index] )

        return candidates

    def getOther(self, char, from_state):
        # Returns the "OTHER" state
        state_index = self.states.index( from_state )
        list = self.transitions[state_index]
        list = [x for x in list if x != from_state]
        other = max(set(list), key=list.count)

        if( other is not None):
            return other
        else:
            self.states.setCurrent( self.states.getStart()[0] )
            candidates = self.getCandidateCharacters(state_index)
            error_msg = BadSequenceException.buildMessage(char, from_state, candidates)
            raise BadSequenceException(error_msg)

class BadSequenceException(Exception):
    def __init__(self, error_msg):
        self.message = error_msg

    def buildMessage(char, from_state, candidates):
        error_msg = "For character=%r from state=%r" %(char, from_state)
        error_msg += " next_state=None."
        error_msg += "\nExpecting one of %r"%(candidates)
        return error_msg
