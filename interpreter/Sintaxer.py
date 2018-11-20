import logging

class Sintaxer(object):

    def __init__(self, symbols_table=None, lexer=None):
        self.logger = logging.getLogger('Sintaxer')
        self.symbols_table = symbols_table
        self.lexer = lexer
        self.current_token = None

    def run():
        self.current_token = self.lexer.nextToken()
        self.checkProgram()

    def checkProgram():
        pass

    def checkHeader():
        pass

    def assignment():
        pass

    def areThereConsts():
        pass

    def defConst():
        pass

    def nextConst():
        pass

    def areThereArrays():
        pass

    def defArray():
        pass

    def nData():
        pass

    def nArray():
        pass

    def checkBody():
        pass

    def instruction():
        pass

    def nInstruction():
        pass

    def function():
        pass

    def parameter():
        pass

    def nParameter():
        pass

    def checkIf():
        pass

    def checkElse():
        pass

    def checkExpr():
        pass

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
