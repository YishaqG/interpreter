import logging
from interpreter.Reader import Reader
from interpreter.Lexer import Lexer
from interpreter.Container import Container

test_path = "./tests/"

def setUp_Logger(log_level):
    # set up logging to file - see previous section for more details
    logging.basicConfig(level=log_level,
                        format='%(name)s:%(levelname)s: %(message)s')

def main():
    setUp_Logger(logging.DEBUG)
    lexer = Lexer()
# setUp_Automata==========================================
    automata_descripter = test_path+"conf/automata_description/1.txt"
    reader = Reader( automata_descripter )
    reader.loadData()
    lexer.setAutomata( reader.getData() )
# setUp_SymbolsTable==========================================
    symbols_table_descripter = test_path+"conf/symbols_table/1.txt"
    reader = Reader( symbols_table_descripter )
    reader.loadData()
    lexer.setSymbolsTable( reader.getData() )
# run_Lexer=======================================
    source = test_path+"source/strings.txt"
    text = None
    with open( source ) as fp:
        text = fp.read()
    lexer.setSource( Container(text) )
    while( True ):
        token = lexer.nextToken()
        print( "\n>>>Token:"+ str(token) )
        input(">>")
        print("\n")

if __name__ == '__main__':
    main()
