def setUpMatrix(height, width, init_value):
    matrix = [init_value]*height
    for i in range(height):
        matrix[i] = [init_value] * width
    return matrix

class Transition(object):
    def __init__(self, rows=None, columns=None):
        self.height = rows
        self.width = columns
        self.table = None

    def __str__(self):
        transitions = "Transitions:\n[\n"
        for row in self.table:
            transitions += "\t"+str(row)+"\n"
        transitions += "]\n"
        return transitions

    def shape(self):
        return (self.height, self.width)

    def __getitem__(self, key):
        if( self.height ):
            return self.table[key]
        else:
            raise Error("Must load transitions.")

    def loadTransitions(self, transitions, alphabet, states):
        self.height = len(states)
        self.width = len(alphabet)
        self.table = setUpMatrix(self.height, self.width, None)
        for transition_function in transitions:
            self.setTransition(transition_function, alphabet, states)

    def setTransition(self, transition_function, alphabet, states):
        if( len(transition_function) <= self.width ):
            from_state = states.index(transition_function[0])
            with_letter = alphabet.index(transition_function[1])
            to_state = transition_function[2]
            self.table[from_state][with_letter] = to_state
        else:
            expected = "<from_state,with_letter,to_state>"
            error_message = "Expected {0} values found {1}".format(expected, transition_function)
            raise ValueError(error_message)
