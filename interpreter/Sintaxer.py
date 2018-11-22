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
            self.logger.info("FUCK_YOU_1")
            self.areThereConsts()
            self.logger.info("FUCK_YOU_2")
            self.areThereArrays()
            self.logger.info("FUCK_YOU_3")
            if(self.current_token == INICIO):
                self.nextToken()
            else:
                self.error(INICIO)
            self.logger.info("FUCK_YOU_4")
            self.checkBody()
            self.nextToken()
            if(self.current_token == FIN):
                self.nextToken()
            else:
                self.error(FIN)
        else:
            self.error(PROGRAMA)

    def checkHeader(self):
        if(self.current_token == PROGRAMA):
            self.nextToken()
            self.match( 'id' )
        else:
            self.error(PROGRAMA)
            #error_msg


    def assignment(self):
        self.idArray()
        self.match('asigna')

    def areThereConsts(self):
        if(self.current_token == CONSTANTES):
            self.nextToken()
            self.defConst()
        elif(self.current_token == ARREGLOS):
            return None
        else:
            self.error(ARREGLOS)
            #manda Error


    def defConst(self):
        self.match('id')
        self.assignment()
        self.typesValues()
        self.nextConst()


    def nextConst(self):
        if(self.current_token == ARREGLOS):
            return None

        self.match('id')
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
        if(self.current_token[0] == 'id' or self.current_token[0] == 'function' or self.current_token[0] == PARA or self.current_token[0] == SI):
            self.instruction()
        else:
            self.error(['id', 'function', PARA, SI])


    def instruction(self):
        if(self.current_token[0] == 'function'):
            self.function()
            self.nInstruction()
        elif(self.current_token == SI):
            self.checkIf()
            self.nInstruction()
        elif(self.current_token == PARA):
            self.checkFor()
            self.nInstruction()
        elif(self.current_token[0] == 'id'):
            self.match('id')
            self.checkExpr()
            self.nInstruction()
        else:
            self.error(['function', 'id', SI, PARA])


    def nInstruction(self):
        if(self.current_token[0] == 'id' or self.current_token[0] == 'function' or self.current_token[0] == 'PARA' or self.current_token[0] == 'SI'):
            self.instruction()
        elif(self.current_token[0] == FIN):
            self.match(FIN)
        else:
            self.error(['function', 'id', FIN])

    def function(self):
        if(self.current_token[0] == 'function'):
            self.nextToken()
            self.match('parentesis_a')
            self.parameter()
            self.match('parentesis_c')
            self.match('punto_coma')
        else:
            self.error(['function','parentesis_a', 'parentesis_c','punto_coma'])


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
            self.error(['id','caracter','entero'])


    def nParameter(self):
        if(self.current_token[0] == 'parentesis_c'):
            return None

        self.match('coma')
        self.nextToken()
        self.typesId()


    def checkIf(self):
        if(self.current_token == SI):
            self.nextToken()
            self.match('parentesis_a')
            self.checkCondition()
            self.match('parentesis_c')
            self.match(ENTONCES)
            self.checkBody()
            self.checkElse()
        else:
            self.error([SI,'parentesis_a','parentesis_c', ENTONCES])


    def checkElse(self):
        if(self.current_token == SINO):
            self.nextToken()
            self.checkBody()
        else:
            self.error(SINO)

    def checkExpr(self):
        if(self.current_token[0] == 'asigna'):
            self.expr()
        elif(self.current_token[0] ==  'punto' or self.current_token[0] == 'corchete_a'):
            self.arrayOp()
        else:
            self.error(['asigna', 'punto', 'corchete_a'])


    def expr(self):
        if(self.current_token[0] == 'corchete_c' or self.current_token[0] == FIN or self.current_token[0] == 'id'):
            return None
        elif(self.current_token[0] == 'function' or self.current_token[0] == PARA or self.current_token[0] == SI):
            return None
        elif(self.current_token[0] == 'asigna'):
            self.match('asigna')
            self.checkOp()
            self.parametersValues()
        else:
            self.error( ['corchete_c', 'function', 'asigna', FIN, SI, PARA])


    def checkFor(self):
        if(self.current_token == PARA):
            self.nextToken()
            self.variableCtrl()
            self.match(HASTA)
            self.parametersValues()
            self.match(PASO)
            self.mm()
            self.match('entero')
            self.match(HACER)
            self.checkBody()
        else:
            self.error([PARA, HASTA, PASO, HACER, 'entero'])

    def variableCtrl(self):
        self.match('id')
        self.nextToken()
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
        elif(self.current_token[0] == 'MOD'):
            self.match('MOD')
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
        if(self.current_token[0] == 'punto'):
            self.lenght()
        elif(self.current_token[0] == 'corchete_a'):
            self.arrayAccess()
        else:
            self.error(['punto', 'corchete_a'])

    def lenght(self):
        self.match('punto')
        self.function()

    def arrayAccess(self):
        if(self.current_token[0] == 'corchete_a'):
            self.match('corchete_a')
            self.index()
            self.match('corchete_c')
        else:
            self.error(['corchete_a'])

    def index(self):
        if(self.current_token[0] == 'id' or self.current_token[0] == 'caracter' or self.current_token[0] == 'entero'):
            self.parametersValues()
            self.expr()
        else:
            self.error(['id', 'caracter', 'entero'])

    def idArray(self):
        if(self.current_token[0] == 'id'):
            self.match('id')
            self.arrayPos()
        else:
            self.error(['id'])

    def arrayPos(self):
        if(self.current_token[0] == 'corchete_a'):
            self.match('corchete_a')
            self.index()
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

    def parametersValues(self):
        if(self.current_token[0] == 'caracter' or self.current_token[0] == 'entero'):
            self.typesValues()

        self.match('id')
        self.idArray()

    def typesValues(self):
        if(self.current_token[0] == 'caracter'):
            self.match('caracter')
        elif(self.current_token[0] == 'entero'):
            self.match('entero')
        else:
            self.error(['caracter', 'entero'])


    def typesId(self):
        if(self.current_token[0] == 'caracter' or self.current_token[0] == 'entero'):
            self.typesValues()
        elif(self.current_token[0] == 'id'):
            self.match('id')
        else:
            self.error(['caracter', 'id', 'entero'])
