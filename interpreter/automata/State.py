from .CustomList import CustomList

KEYS = ['states', 'start_states', 'final_states']
class State(CustomList):

    def __init__(self, data):
        super().__init__( data[KEYS[0]][0] )
        self.start = None
        self.final = None
        self.loadStates(data)
        self.current = self.start[0]
        self.next_state = None

    def __str__(self):
        states = "States:\n%r\n" % (self)
        start = "\tStart:\t{0}".format(self.start)
        final = "\tFinal:\t{0}\n".format(self.final)
        return states+start+final

    def loadStates(self, data):
        self._validateDict(data)
        self.setStart( data[KEYS[1]][0] )
        self.setFinal( data[KEYS[2]][0] )

    def _validateDict(self, data):
        for key in KEYS:
            if( key not in data ):
                error_msg = "Unable to load <States> from %r" % data
                raise Error(error_msg)

    def setStart(self, start):
        if( isinstance(start, list)  ):
            if( start in self ):
                self.start = start
        else:
            raise TypeError(start)

    def setFinal(self, final):
        if( isinstance(final, list)  ):
            if( final in self ):
                self.final = final
        else:
            raise TypeError(final)

    def getStart(self):
        return self.start

    def getFinal(self):
        return self.final

    def setCurrent(self, state):
        self.current = state

    def getCurrent(self):
        return self.current

    def isFinal(self, to_eval):
        if( to_eval in self.final ):
            return to_eval
        return None
