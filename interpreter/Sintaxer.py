import logging
from interpreter.Container import EndOfFileException

ARREGLOS = ('reserved_word', 'ARREGLOS')
PROGRAMA = ('reserved_word', 'PROGRAMA')
CONSTANTES = ('reserved_word', 'CONSTANTES')
HASTA = ('reserved_word', 'HASTA')
HACER = ('reserved_word', 'HACER')
MOD = ('reserved_word', 'MOD')
ENTONCES = ('reserved_word', 'ENTONCES')
INICIO = ('reserved_word', 'INICIO')
FIN = ('reserved_word', 'FIN')
PARA = ('reserved_word', 'PARA')
SI = ('reserved_word', 'SI')
SINO = ('reserved_word', 'NOSI')
PASO = ('reserved_word', 'PASO')

class Sintaxer(object):

    def __init__(self, symbols_table=None, lexer=None):
        self.logger = logging.getLogger('Sintaxer')
        self.symbols_table = symbols_table
        self.lexer = lexer
        self.current_token = None
        self.current_line = None
        self.instruction = []

    def nextToken(self):
        token = self.lexer.nextToken()
        self.logger.debug("Evaluating token: " + str(token))
        self.current_token = token[:2]
        if( self.current_line != token[2]):
            self.current_line = token[2]

    def error(self, expected):
        error_msg = "Expected %r found %r" %(expected, self.current_token)
        error_msg += " at line %r" % self.current_line
        self.logger.error(error_msg)
        raise SyntacticError()

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
            self.logger.info("Header Checked")
            self.areThereConsts()
            self.logger.info("Constants Checked")
            self.areThereArrays()
            self.logger.info("Arrays Checked")
            if(self.current_token == INICIO):
                self.nextToken()
            else:
                self.error(INICIO)
            self.logger.info("Program start")
            self.checkBody()
            self.logger.info("Body checked")
            if(self.current_token == FIN):
                self.nextToken()
            else:
                self.error(FIN)
            self.logger.info("Program end")
        else:
            self.error(PROGRAMA)

    def checkHeader(self):
        if(self.current_token == PROGRAMA):
            self.nextToken()
            self.match( 'id' )
        else:
            self.error(PROGRAMA)

    def assignment(self):
        temp = []
        temp += self.idArray()
        self.match('asigna')

        return temp

    def areThereConsts(self):
        if(self.current_token == CONSTANTES):
            self.nextToken()
            self.defConst()
        elif(self.current_token == ARREGLOS):
            return None
        else:
            self.error(ARREGLOS)

    def defConst(self):
        temp = []
        temp += self.assignment()
        temp.append( self.typesValues() )
        self.semantic.defConst(temp)
        self.nextConst()

    def nextConst(self):
        if(self.current_token == ARREGLOS):
            return None

        self.defConst()

    def areThereArrays(self):
        if(self.current_token == ARREGLOS):
            self.nextToken()
            self.defArray()
        elif(self.current_token == INICIO):
            return None
        else:
            self.error([ARREGLOS, INICIO])

    def defArray(self):
        temp = []
        self.assignment()
        self.match('llave_a')
        temp.append( self.nData() )
        self.match('llave_c')
        self.semantic.defArray(temp)
        self.nArray()

    def nData(self):
        if(self.current_token[0] == 'llave_c'):
            return None

        temp = []
        self.match('coma')
        temp.append(self.typesId())
        hasNData = self.nData()
        if( hasNData is not None ):
            temp.append( hasNData )

    def nArray(self):
        if(self.current_token[0] == 'id'):
            self.defArray()

        elif(self.current_token == INICIO):
            return None

        else:
            self.error(['id', INICIO])

    def checkBody(self):
        self.logger.info('checkBody')
        predict = self.current_token[0] in ['id', 'function']
        itIs = self.current_token in [PARA, SI]
        if( predict or itIs ):
            self.instruction()
            self.nInstruction()
        else:
            self.error(['id', 'function', PARA, SI])

    def instruction(self):
        self.logger.info('instruction')
        if(self.current_token[0] == 'function'):
            self.function()
        elif(self.current_token == SI):
            self.checkIf()
        elif(self.current_token == PARA):
            self.checkFor()
        elif(self.current_token[0] == 'id'):
            self.checkExpr()
        else:
            self.error( ['function', 'id', SI, PARA] )

    def nInstruction(self):
        self.logger.info('nInstruction')
        predict = ['id', 'function']
        itIs = (self.current_token == PARA) or (self.current_token == SI)
        if((self.current_token[0] in predict) or itIs):
            self.checkBody()
        else:
            return None

    def function(self):
        self.logger.info('function')
        if(self.current_token[0] == 'function'):
            self.nextToken()
            self.match('parentesis_a')
            self.parameter()
            self.match('parentesis_c')
            self.match('punto_coma')
        else:
            self.error(['function','parentesis_a', 'parentesis_c','punto_coma'])

    def parameter(self):
        predict = ['id', 'caracter', 'entero']
        if( self.current_token[0] in predict):
            self.typesId()
            self.nParameter()
        else:
            self.error( predict )

    def nParameter(self):
        if(self.current_token[0] == 'parentesis_c'):
            return None

        self.match('coma')
        self.typesId()

    def checkIf(self):
        self.logger.info('checkIf')
        if(self.current_token == SI):
            self.nextToken()
            self.match('parentesis_a')
            self.checkCondition()
            self.match('parentesis_c')
            if(self.current_token == ENTONCES):
                self.nextToken()
            else:
                self.error(ENTONCES)
            self.checkBody()
            self.checkElse()
        else:
            self.error([SI,'parentesis_a','parentesis_c', ENTONCES])

    def checkElse(self):
        self.logger.info('checkElse')
        if(self.current_token == SINO):
            self.nextToken()
            self.checkBody()
        elif(self.current_token == FIN):
            self.nextToken()
        else:
            self.error( [SINO, FIN] )

    def checkExpr(self):
        self.logger.info('checkExpr')
        temp = []
        temp.append(self.current_token[1])
        if(self.current_token[0] == 'id'):
            self.match('id')
            temp += self.checkSubExpr()
            self.match('punto_coma')
            print(temp)
        else:
            self.error('id')

        return temp

    def checkSubExpr(self):
        temp = []
        if(self.current_token[0] == 'asigna'):
            temp += self.add()
        elif(self.current_token[0] == 'corchete_a'):
            self.arrayAccess()
            self.add()
        else:
            self.error(['asigna', 'corchete_a'])

        return temp

    def add(self):
        temp = []
        temp.append(self.current_token[1])
        if(self.current_token[0] == 'asigna'):
            self.match('asigna')
            self.parametersValues()
            temp += self.expr()
        else:
            self.error('asigna')

    def expr(self):
        predict = ['suma', 'div_entera', 'resta', 'mult']
        if((self.current_token[0] in predict) or self.current_token == MOD):
            self.checkOp()
            self.parametersValues()
        elif( self.current_token[0] in ['punto_coma', 'corchete_c'] ):
            return None
        else:
            self.error( predict + ['punto_coma', 'corchete_c'] + MOD )

    def checkFor(self):
        self.logger.info('checkFor')
        if(self.current_token == PARA):
            self.nextToken()
            self.variableCtrl()
            if( self.current_token == HASTA):
                self.nextToken()
            else:
                self.error(HASTA)
            self.parametersValues()
            if( self.current_token == PASO):
                self.nextToken()
            else:
                self.error(PASO)
            self.mm()
            self.match('entero')
            if( self.current_token == HACER):
                self.nextToken()
            else:
                self.error(HACER)
            self.checkBody()
            if( self.current_token == FIN):
                self.nextToken()
            else:
                self.error(FIN)
        else:
            self.error([PARA, HASTA, PASO, HACER, 'entero'])

    def variableCtrl(self):
        self.match('id')
        self.ToCtrl()

    def ToCtrl(self):
        if(self.current_token == HASTA):
            return None

        self.match('asigna')
        self.parametersValues()

    def mm(self):
        if(self.current_token[0] == 'resta'):
            self.match('resta')
        elif(self.current_token[0] == 'suma'):
            self.match('suma')
        else:
            self.error(['resta', 'suma'])

    def checkOp(self):
        if(self.current_token[0] == 'mult'):
            self.match('mult')
        elif(self.current_token[0] == 'div_entera'):
            self.match('div_entera')
        elif(self.current_token[1] == 'MOD'):
            self.nextToken()
        elif(self.current_token[0] == 'suma'):
            self.mm()
        elif(self.current_token[0] == 'resta'):
            self.mm()
        else:
            self.error(['mult', 'div_entera', 'MOD', 'suma', 'resta'])

    def checkCondition(self):
        if(self.current_token[0] == 'id' or self.current_token[0] == 'caracter' or self.current_token[0] == 'entero'):
            self.parametersValues()
            self.condition()
            self.parametersValues()
        else:
            self.error(['id', 'caracter', 'entero'])

    def condition(self):
        if(self.current_token[0] == 'igual_a'):
            self.match('igual_a')
        elif(self.current_token[0] == 'menor'):
            self.match('menor')
        elif(self.current_token[0] == 'menor_igual'):
            self.match('menor_igual')
        elif(self.current_token[0] == 'mayor'):
            self.match('mayor')
        elif(self.current_token[0] == 'mayor_igual'):
            self.match('mayor_igual')
        elif(self.current_token[0] == 'diferente'):
            self.match('diferente')
        else:
            self.error(['igual_a', 'menor', 'menor_igual', 'mayor', 'menor_igual', 'diferente'])

    def arrayOp(self):
        temp = []
        temp.append('array_access')
        if(self.current_token[0] == 'punto'):
            temp += self.lenght()
        elif(self.current_token[0] == 'corchete_a'):
            temp += self.arrayAccess()
        else:
            self.error(['punto', 'corchete_a'])

        return temp

    def lenght(self):
        temp = []
        self.match('punto')
        if(self.current_token[1] == 'lenght'):
            self.nextToken()
            temp.append( 'LEN' )
        else:
            self.error('lenght')

        return temp

    def arrayAccess(self):
        temp = []
        if(self.current_token[0] == 'corchete_a'):
            self.match('corchete_a')
            temp += self.index()
            self.match('corchete_c')
            temp.append('array_access')
        else:
            self.error(['corchete_a'])

        return temp

    def index(self):
        temp = []
        if(self.current_token[0] == 'id' or self.current_token[0] == 'caracter' or self.current_token[0] == 'entero'):
            temp += self.parametersValues()
            temp += self.expr()
        else:
            self.error(['id', 'caracter', 'entero'])

    def idArray(self):
        temp = []
        if(self.current_token[0] == 'id'):
            temp.append( self.current_token )
            self.match('id')
            hasArrayAccess = self.arrayPos()
            if( hasArrayAccess is not None ):
                temp.append( hasArrayAccess )
        else:
            self.error(['id'])

        return temp

    def arrayPos(self):
        temp = None
        if(self.current_token[0] == 'corchete_a'):
            self.match('corchete_a')
            temp = self.index()
            self.match('corchete_c')
        elif(self.current_token[0] == 'asigna' or self.current_token[0] == 'igual_a' or self.current_token[0] == 'menor'):
            return None
        elif(self.current_token[0] == 'menor_igual' or self.current_token[0] == 'mayor' or self.current_token[0] == 'mayor_igual'):
            return None
        elif(self.current_token[0] == 'diferente' or self.current_token[0] == PASO or self.current_token[0] == 'parentesis_c'):
            return None
        elif(self.current_token[0] == 'corchete_c' or self.current_token[0] == HASTA or self.current_token[0] == FIN or self.current_token[0] == 'id'):
            return None
        elif(self.current_token[0] == 'function' or self.current_token[0] == PARA or self.current_token[0] == SI):
            return None
        else:
            self.error(['TO_DO'])

        return temp

    def parametersValues(self):
        temp  = []
        if( self.current_token[0] == 'id'):
            temp.append( self.current_token )
            self.match('id')
            temp += self.fromID()
        elif(self.current_token in ['caracter', 'entero']):
            temp.append( self.typesValues() )
        else:
            self.error( ['id', 'caracter', 'entero'] )

        return temp

    def fromID(self):
        temp = []
        toEpsilon = ['igual_a', 'menor', 'menor_igual', 'mayor', 'mayor_igual', 'diferente', 'mult', 'div_entera', 'MOD', 'suma', 'resta', 'parentesis_c', 'corchete_c', 'punto_coma']
        if(self.current_token[0] == 'corchete_a'):
            temp += self.arrayPos()
        elif(self.current_token[0] == 'punto'):
            temp += self.lenght()
        elif( (self.current_token[0] in toEpsilon) or (self.current_token in [HASTA, PASO])):
            return None
        else:
            predict = toEpsilon + [HASTA, PASO, 'corchete_a', 'punto']
            self.error(predict)

        return temp

    def typesValues(self):
        temp = self.current_token
        if(self.current_token[0] == 'caracter'):
            self.match('caracter')
        elif(self.current_token[0] == 'entero'):
            self.match('entero')
        else:
            self.error(['caracter', 'entero'])

        return temp

    def typesId(self):
        temp = None
        if(self.current_token[0] == 'caracter' or self.current_token[0] == 'entero'):
            temp = self.typesValues()
        elif(self.current_token[0] == 'id'):
            temp = self.current_token
            self.match('id')
        else:
            self.error(['caracter', 'id', 'entero'])

        return temp

class SyntacticError(Exception):
    def __init__(self):
        pass
