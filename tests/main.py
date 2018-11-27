import logging
from interpreter.Container import Container
from interpreter.Reader import Reader
from interpreter.SymbolsTable import SymbolsTable
from interpreter.automata.Automata import Automata
from interpreter.Lexer import Lexer
from interpreter.Sintaxer import Sintaxer, SyntacticError

test_path = "./config/"

def setUp_Logger(log_level):
    # set up logging to file - see previous section for more details
    logging.basicConfig( level=log_level,
                        format='%(name)s:%(levelname)s: %(message)s')

def setUp_SymbolsTable():
    symbols_table_descripter = test_path+"/symbols_table/PF.txt"
    reader = Reader( symbols_table_descripter )
    reader.loadData()
    symbols_table = SymbolsTable()
    symbols_table.loadFromDict( reader.getData() )
    symbols_table.addFunction( 'ESCRIBE', ['nada'] ) # 'nada' because it should print anything
    symbols_table.addFunction( 'LEE', ['apuntador'] )

    return symbols_table

def setUp_Automata():
    automata_descripter = test_path+"/automata/PF.txt"
    reader = Reader( automata_descripter )
    reader.loadData()
    automata = Automata()
    automata.loadFromDict( reader.getData() )

    return automata

def setUp_Lexer(symbols_table, automata, text):
    lexer = Lexer()
    lexer.setSymbolsTable( symbols_table )
    lexer.setAutomata( automata )
    lexer.setSource( Container(text) )
    return lexer

def getSourceText():
    source = "./tests/input/PF_pares.txt"
    text = None
    with open( source ) as fp:
        text = fp.read()
    return text

def main():
    setUp_Logger(logging.DEBUG)

    symbols_table = setUp_SymbolsTable()
    print(symbols_table)
    automata = setUp_Automata()
    text = getSourceText()
    lexer = setUp_Lexer(symbols_table, automata, text)

# run_Sintaxer=======================================
    stn = Sintaxer(symbols_table, lexer)
    try:
        print("Syntactic analysis starts")
        stn.run()
        print("Syntactic analysis ended")
    except SyntacticError:
        pass

if __name__ == '__main__':
    main()
