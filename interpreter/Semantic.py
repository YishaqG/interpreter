import logging
from interpreter import Lexer

Instrucciones:
    -Se ejecutaran la 1a vez
    -Se agregaran a una lista cuando formen parte de un ciclo
        -Se ejecutaran n-1 veces
        -Terminaran de agregarse cuando se encuentre el FIN
Condicionales:
    -Se ignoraran todas las instrucciones consiguientes cuando la condicion no se cumpla
        -Se recibiran e ignoraran instrucciones hasta un NOSI o FIN

MAQUINA DE ESTADOS!!!

class Semantic(object):
    def __init__(self, sT):
        self.symbols_table = sT
        self.current_state = 0
        self.subSM = Semantic()

    def defConst(self, inst):
        NAME = 0
        VALUE = 1
        if( not self.symbols_table.getCONST( inst[NAME][Lexer.Token.LEXEME.value] ) ):
            self.symbols_table.addCONST(
                inst[VALUE][Lexer.Token.TYPE.value],
                inst[NAME][Lexer.Token.LEXEME.value],
                inst[VALUE][Lexer.Token.LEXEME.value]
                )

    def defArray(self, inst):
        NAME = 0
        VALUE = 1
        inst[NAME][Lexer.Token.LEXEME.value] = inst[NAME][Lexer.Token.LEXEME.value].lower()
        if( not self.symbols_table.getID( inst[NAME][Lexer.Token.LEXEME.value] ) ):
            self.symbols_table.addID(
                'array',
                inst[NAME][Lexer.Token.LEXEME.value],
                inst[VALUE][Lexer.Token.LEXEME.value]
            )

    def function(self, inst):
        NAME = 0
        VALUE = 1
        if( inst[NAME][Lexer.Token.LEXEME.value] == "ESCRIBE" ):
            self.logger.setFormatter( logging.Formatter('%(message)s') )
            idValue = self.getIDValue( inst[VALUE] )
            if(idValue is not None):
                self.logger.info( idValue[2] )
            else:
                self.logger.info( inst[VALUE][Lexer.Token.LEXEME.value] )
            self.logger.setFormatter( logging.Formatter('%(name)s:%(levelname)s: %(message)s') )
        else:
            if( inst[VALUE][Lexer.Token.TYPE.value] == 'identifier' )
                idValue = self.getIDValue( inst[VALUE] )
                if(idValue is not None):
                    input_value = None
                    if( (idValue[0] == 'caracter') and input_value.isalpha() and len(input_value) == 1 ):
                        self.symbols_table.addID( idValue[0], id_value[1], input_value  )
                    elif( (idValue[0] == 'entero') and input_value.isdigit() ):
                        self.symbols_table.addID( idValue[0], id_value[1], int(input_value)  )
                    else:
                        error_msg = "Variable type=%r found %r" %(idValue[0], input_value)
                        self.logger.error(error_msg)
                else:
                    error_msg = "Not previous declaration of <identifier> %r" %(inst[VALUE][Lexer.Token.LEXEME.value])
                    self.logger.error(error_msg)
            else:
                error_msg = "Must be <identifier> not %r" %(inst[VALUE][Lexer.Token.TYPE.value])
                self.logger.error(error_msg)

    def getIDValue(self, id):
        if( id[Lexer.Token.TYPE.value] == 'identifier' ):
            id = self.symbols_table.getID( id[Lexer.Token.LEXEME.value] )
            if( id is not None ):
                return id


    def transitions(self, inst):
        if(self.current_state == 0):
            self.start(inst)
        elif(self.current_state == 1):
            if(inst[0] == 'FIN'):
                self.current_state = 4
                self.transitions(inst)
            else:
                self.inst()
        elif(self.current_state == 2):
            if( self.subSM.transitions(inst) ):
                self.current_state = 3
                self.transitions(inst)
        elif(self.current_state == 3):
            if(inst[0] == 'FIN'):
                self.current_state = 4
                self.transitions(inst)
        elif(self.current_state == 4):
            self.subSM = StateMachine()
            return True # It has finished
        elif(self.current_state == 5):
            if( self.subSM.transitions(inst) || (inst[0] == 'SINO') ):
                self.current_state = 6
                self.transitions(inst)
        elif(self.current_state == 6):
            if(inst[0] == 'FIN'):
                self.current_state = 4
                self.transitions(inst)
            elif( inst[0] == 'SINO' ):
                self.subSM = StateMachine()
                self.current_state = 2

        return False # It has not finished

    def start(self, inst):
        if( inst[0] == 'PARA' ):
            self.current_state = 2
        elif( inst[0] == 'SI' ):
            self.current_state = 5
        else:
            self.current_state = 1

        self.transitions(inst)

    def inst(self, inst):
        # ID: LALALALAND!
        if()


    def para(self, inst):
        self.current_state = 2
        self.stateMachine()
