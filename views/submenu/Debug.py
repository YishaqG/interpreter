import sys, logging
from tkinter import *
from tkinter.filedialog import *
from tkinter.messagebox import *
from interpreter.Reader import Reader
from interpreter.Lexer import Lexer
from interpreter.Container import Container

logger = logging.getLogger(__name__)

class Debug():
    def __init__(self, text):
        self.text = text
        self.lexer = Lexer()

    def loadAutomata(self):
        f = askopenfile(mode='r')
        reader = Reader(f.name)
        reader.loadData()
        self.lexer.setAutomata( reader.getData() )

    def loadSymbolsTable(self):
        f = askopenfile(mode='r')
        reader = Reader(f.name)
        reader.loadData()
        self.lexer.setSymbolsTable( reader.getData() )

    def run(self):
        t = self.text.get(0.0, END)
        self.lexer.setSource( Container(t) )
        while(True):
            token = self.lexer.nextToken()
            logger.info( token )


def setUp(menubar, interpreter):
    menu = Menu(menubar, tearoff=0)
    menu.add_command(label="Load Automata", command=interpreter.loadAutomata)
    menu.add_command(label="Load Symbols Table", command=interpreter.loadSymbolsTable)
    menu.add_separator()
    menu.add_command(label="Run", command=interpreter.run)
    menubar.add_cascade(label="Interpreter", menu=menu)

if __name__ == "__main__":
	print ("Please run 'main.py'")
