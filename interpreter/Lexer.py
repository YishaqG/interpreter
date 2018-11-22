import logging
from .automata.Automata import Automata
from .automata.Automata import BadSequenceException
from . import SymbolsTable
from .Container import Container



ID = 0
LEXEME = 1

class Lexer(object):
    def __init__(self, symbols_table=None, automata=None, source=None):
        self.logger = logging.getLogger('Lexer')
        self.source = source
        self.automata = automata
        self.symbols_table = symbols_table

    def setSource(self, source):
        if( isinstance(source, Container) ):
            self.source = source
        else:
            raise TypeError(source)

    def setSymbolsTable(self, table):
        if( isinstance(table, SymbolsTable.SymbolsTable) ):
            self.symbols_table = table
        elif(isinstance(table, dict)):
            self.symbols_table = SymbolsTable.SymbolsTable()
            self.symbols_table.loadFromDict(table)
        else:
            raise TypeError(alphabet)

    def setAutomata(self, automata):
        if( isinstance(automata, Automata) ):
            self.automata = automata
        elif(isinstance(automata, dict)):
            self.automata = Automata()
            self.automata.loadFromDict(automata)
        else:
            raise TypeError(alphabet)

    def nextChar(self):
        current_char = self.source.nextChar()
        while( current_char.isspace() ):
            current_char = self.source.nextChar()
        return current_char

    def _whiteSpaceHandler(self):
        current_char = self.source.nextChar()
        while( current_char.isspace() ):
            current_char = self.source.nextChar()
        self.source.recoilChar(1)

    def nextToken(self):
        tuple = None
        try:
            result = self._evalNextString()
            tuple = self._classify(result)
        except ValueError as e:
            error_msg = "Invalid character {0} at {1}.".format(
                str(e)[:3],
                self.source.getCoordinates()
                )
            self.logger.error(error_msg)
        except BadSequenceException as e:
            error_msg = "Invalid sequence at found at {0}\n".format(
                self.source.getCoordinates()
                )
            error_msg += str(e)
            self.logger.error(error_msg)

        return tuple

    def _evalNextString(self):
        self._whiteSpaceHandler()
        self.automata.restart()

        current_char = self.source.nextChar()
        evaluation = self.automata.evaluate( current_char.lower() )
        lexeme = current_char

        if( evaluation is None ):
            while( True ):
                current_char = self.source.nextChar()
                lexeme += current_char

                if( current_char.isspace() ):
                    evaluation = self.automata.evaluate( None )
                    break

                try:
                    evaluation = self.automata.evaluate( current_char.lower() )
                except BadSequenceException:
                    if( evaluation is not None ):
                        break
                    else:
                        pass
                except ValueError:
                    evaluation = self.automata.evaluate( None )
                    break

                if( self.symbols_table.isReservedWord(lexeme) ):
                    evaluation = SymbolsTable.Types.RESERVED_WORDS.value
                    break
                elif( self.symbols_table.isFunction(lexeme) ):
                    evaluation = SymbolsTable.Types.FUNCTIONS.value
                    break
                elif(evaluation is not None):
                    break

        return (evaluation, lexeme)

    def _classify(self, data):
        tuple = None
        self.logger.debug("Classifier.ResivedData="+str(data))
        itIs = (    (data[ID] is SymbolsTable.Types.RESERVED_WORDS.value)
                    or (data[ID] is SymbolsTable.Types.FUNCTIONS.value)
                )
        if( itIs ):
            tuple = (
                data[ID],
                data[LEXEME],
                self.source.getRowIndex()
                )
        elif( data[ID] is not None ):
            token_info = self.symbols_table.getToken( data[ID] )
            recoil = int(token_info[SymbolsTable.Token.RECOIL.value])
            self.source.recoilChar( recoil )
            tuple = (
                token_info[SymbolsTable.Token.NAME.value],
                data[LEXEME][:-recoil] if recoil > 0 else data[LEXEME],
                self.source.getRowIndex()
                )
        else:
            self.logger.error("Unknown token.")

        return tuple
