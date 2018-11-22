import logging

ARREGLOS = ('reserved_word', 'ARREGLOS')
PROGRAMA = ('reserved_word', 'PROGRAMA')
CONSTANTES = ('reserved_word', 'CONSTANTES')
INICIO = ('reserved_word', 'INICIO')
FIN = ('reserved_word', 'FIN')
PARA = ('reserved_word', 'PARA')
SI = ('reserved_word', 'SI')
SINO = ('reserved_word', 'SINO')

class Sintaxer(object):

    def __init__(self, symbols_table=None, lexer=None):
        self.logger = logging.getLogger('Sintaxer')
        self.symbols_table = symbols_table
        self.lexer = lexer
        self.current_token = None

    def nextToken(self):
        self.current_token = self.lexer.nextToken()[:2]

    def error(self, expected):
        error_msg = "Expected %r found %r" %(expected, self.current_token)
        self.logger.error(error_msg)
        #TODO Raise error counter

    def match(self, terminal):
        if( terminal == self.current_token[0] ):
            self.nextToken()
        else:
            self.error(terminal)

    def run(self):
        try:
            self.nextToken()
            self.checkProgram()
        except EndOfFileException as ex:
            return True

        return False

    def checkProgram(self):
        if(self.current_token == PROGRAMA):
            self.checkHeader()
            self.areThereConsts()
            self.areThereArrays()
            if(self.current_token == INICIO)
                self.nextToken()
                self.checkBody()
                if(self.current_token == FIN):
                    self.nextToken()
                else:
                    self.error( FIN )
            else:
                self.error( INICIO )
        else:
            self.error( PROGRAMA )

    def checkHeader(self):
        if(self.current_token == PROGRAMA):
            self.nextToken()
            self.match( 'id' )
        else:
            self.error( PROGRAMA )

    def assignment(self):
        if(self.current_token[0] == 'id'):
            self.idArray()
            self.match('asigna')
        else:
            self.error('id')

    def areThereConsts(self):
        if(self.current_token == CONSTANTES):
            self.nextToken()
            self.defConst()
        elif(self.current_token == ARREGLOS):
            pass
        else:
            self.error([CONSTANTES, ARREGLOS])

    def defConst(self):
        if(self.current_token[0] == 'id'):
            self.assignment()
            self.typesValues()
            self.nextConst()

    def nextConst(self):
        if(self.current_token == ARREGLOS):
            return None
        elif(self.current_token[0] == 'id'):
            self.defConst()
        else:
            self.error([ARREGLOS, id])

    def areThereArrays(self):
        if(self.current_token == ARREGLOS):
            self.nextToken()
            self.defArray()
        elif(self.current_token == INICIO):
            return None
        else:
            self.error([ARREGLOS, INICIO])


    def defArray(self):
        if(self.current_token[0] == 'id'):
            self.assignment()
            self.match('llave_a')
            self.typesId()
            self.nData()
            self.match('llave_c')
            self.nArray()


    def nData(self):
        if(self.current_token[0] == 'llave_c'):
            return None

        self.match('coma')
        self.typesId()
        self.nData()

    def nArray(self):
        if(self.current_token[0] == 'id'):
            self.defArray()
        elif(self.current_token == INICIO):
            return None
        else:
            self.error(['id', INICIO])

    def checkBody(self):
        if(self.current_token[0] == 'function'):
            self.instruction()
            self.nInstruction()
        elif(self.current_token == PARA):
            self.instruction()
            self.nInstruction()
        elif(self.current_token == SI):
            self.instruction()
            self.nInstruction()
        elif(self.current_token[0] == 'id'):
            self.instruction()
            self.nInstruction()
        else:
            self.error(['function', PARA, SI, 'id'])

    def instruction(self):
        if(self.current_token[0] == 'function'):
            self.function()
        elif(self.current_token == SI):
            checkIf()
        elif(self.current_token == PARA):
            checkFor():
        elif(self.current_token[0] == 'id'):
            self.nextToken()
            self.checkExpr()
        else:
            self.error('function', SI, PARA, 'id')

    def checkExpr(self):
        if(self.current_token[0] == 'asigna'):
            self.expr()
        elif(self.current_token[0] == 'punto'):
            self.arrayOp()
        elif(self.current_token[0] == 'corchete_a'):
            self.arrayOp()
        else:
            self.error(['asigna', 'punto', 'corchete_a'])

    def nInstruction(self):
        if(self.current_token[0] == 'id'):
            self.instruction()
        elif(self.current_token[0] == 'function'):
            self.instruction()
        elif(self.current_token == PARA):
            self.instruction()
        elif(self.current_token == SI):
            self.instruction()
        elif(self.current_token == FIN):
            return None
        elif(self.current_token == SINO):
            return None
        elif(self.current_token == PARA):
            return None
        elif(self.current_token == SI):
            return None
        elif(self.current_token[0] == 'id'):
            return None
        elif(self.current_token[0] == 'function'):
            return None
        else:
            self.error([SI, SINO, FIN, PARA, 'id', 'function'])

     def function(self):

     def parameter(self):
        if(self.current_token[0] == 'id'):
            self.typesId()
            self.nParameter()
        elif(self.current_token[0] == 'caracter'):
            self.typesId()
            self.nParameter()
        elif(self.current_token[0] == 'entero'):
            self.typesId()
            self.nParameter()

        else:
            pass


    def nParameter(self):
        if(self.current_token[0] == 'coma'):
            self.match('coma')
            self.typesId()

        elif(self.current_token[0] == 'parentesis_c'):
            return None

        else:
            pass


    def checkIf(self):
        if(self.current_token == SI):
            self.match('parentesis_a')
            self.checkCondition()
            self.match('parentesis_c')
            self.checkBody()
            self.checkElse()
        else:
            pass


    def checkElse(self):
        if(self.current_token == SINO):
            self.checkBody()
        elif(self.current_token == FIN):
            pass
        else:
            pass

    def checkExpr(self):
        self.match('id')
        self.assignment()
        self.parametersValues()
        self.expr()
        self.match('punto_coma')

    def expr():
        pass

    def checkFor():
        pass

    def variableCtrl():
        pass

    def mm():
        pass

    def checkOp():
        pass

    def checkCondition():
        pass

    def condition():
        pass

    def arrayOp():
        pass

    def lenght():
        pass

    def arrayAccess():
        pass

    def index():
        pass

    def idArray():
        pass

    def arrayPos():
        pass

    def parametersValues():
        pass

    def typesValues():
        pass

    def typesId():
        pass
