from enum import Enum

class Token(Enum):
    RECOIL = 1
    NAME = 0

class Types(Enum):
    TOKENS = 'tokens'
    RESERVED_WORDS = 'reserved_word'

KEYS = ['tokens', 'reserved_words']
class SymbolsTable(object):

    def __init__(self):
        self.table = {}
        self.table[Types.TOKENS.value] = {}
        self.table[Types.RESERVED_WORDS.value] = []

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
        print(self)

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
