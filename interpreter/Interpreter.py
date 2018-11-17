from interpreter.automata import Automata
from interpreter import Reader, Lexer, Container

class Interpreter(object):
    def __init__(self):
        self.automata = None
        self.text = None

    def setAutomata(self, automata):
        if( isinstance(automata, Automata) ):
            self.automata = automata
        elif(isinstance(automata, dict)):
            self.automata = Automata()
            self.automata.loadFromDict(automata)
        else:
            raise TypeError(alphabet)

    def getAutomata(self):
        return self.automata
