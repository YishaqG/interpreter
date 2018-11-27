from enum import Enum

class Token(Enum):
    NAME = 0
    RECOIL = 1

class Function(Enum):
    NAME = 0
    PARAMETERS = 1

class Types(Enum):
    TYPES = 'type'
    TOKENS = 'tokens'
    RESERVED_WORDS = 'reserved_word'
    FUNCTIONS = 'function'
    IDS = 'identifier'
    CONSTS = 'constant'

KEYS = ['tokens', 'reserved_words']
class SymbolsTable(object):
    def __init__(self):
        self.table = {}
        self.table[Types.TYPES.value] = ['entero', 'caracter', 'arreglo', 'nada', 'apuntador']
        self.table[Types.TOKENS.value] = {}
        self.table[Types.RESERVED_WORDS.value] = []
        self.table[Types.FUNCTIONS.value] = {}
        self.table[Types.IDS.value] = {}
        self.table[Types.CONSTS.value] = {}

    def __str__(self):
        return "Symbols Table:\t"+str(self.table)+"\n"

    def _validateDict(self, data):
        for key in KEYS:
            if( key not in data ):
                error_msg = "Unable to load <Symbols Table> from %r" % data
                raise Error(error_msg)

    def loadFromDict(self, data):
        self._validateDict(data)
        self.loadToken( data[KEYS[0]] )
        self.loadReservedWords( data[KEYS[1]][0] )

    def loadToken(self, data):
        for token in data:
            self.addToken(token[0], token[1:])

    def addToken(self, key, value):
        self.table[Types.TOKENS.value][key] = value

    def getToken(self, to_get):
        return self.table[Types.TOKENS.value][to_get]

    def loadReservedWords(self, data):
        self.table[Types.RESERVED_WORDS.value] = data

    def addReservedWord(self, key_word):
        self.table[Types.RESERVED_WORDS.value].append(key_word)

    def isReservedWord(self, key_word):
        return key_word in self.table[Types.RESERVED_WORDS.value]

    def addFunction(self, name, parameters):
        if( not isinstance(parameters, list) ):
            raise TypeError( parameters )
        for type in parameters:
            if( not type in self.table[Types.TYPES.value] ):
                error_msg = "Value=%r, not in %r" %(type, self.table[Types.TYPES.value])
                raise LookupError(error_msg)

        self.table[Types.FUNCTIONS.value][name] = parameters

    def isFunction(self, name):
        return name in self.table[Types.FUNCTIONS.value]

    def addID(self, type, name, value):
        self.table[Types.IDS.value][name] = [type, value]

    def getID(self, name):
        return self.table[Types.IDS.value][name]

    def addCONST(self, type, name, value):
        self.table[Types.CONSTS.value][name] = [type, value]

    def getCONST(self, name):
        return self.table[Types.CONSTS.value][name]
