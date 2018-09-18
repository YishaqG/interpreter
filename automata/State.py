from .CustomList import CustomList

class State(CustomList):
    def __init__(self, l, start, end):
        super().__init__( l )
        self.start = None
        self.end = None
        self.__setStart(start)
        self.__setFinal(end)
        self.current = start

    def __str__(self):
        states = "States:\t%r\n" % (self)
        start = "\tStart:{0}".format(self.start)
        end = "\tEnd:{0}\n".format(self.end)
        return states+start+end

    def __setStart(self, start):
        if( isinstance(start, list)  ):
            if( start in self ):
                self.start = start
        else:
            raise TypeError(start)

    def __setFinal(self, end):
        if( isinstance(end, list)  ):
            if( end in self ):
                self.end = end
        else:
            raise TypeError(end)

    def setCurrent(self, current):
        if( current in self ):
            self.current = current

    def getStart(self):
        return self.start

    def getFinal(self):
        return self.end

    def getCurrent(self):
        return self.current
