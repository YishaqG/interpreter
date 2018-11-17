import re
from pathlib import Path

READER_DESCRIPTION = {
    'keys': '(?<=^@)\w+$',
    'values': '[^ \t\n]+'
}

def isValidPath(path):
    if( isinstance(path, Path) ):
        if( not path.exists() ):
            raise FileNotFoundError()
        else:
            return True
    else:
        return isValidPath( Path(path) )

class Splitter(object):
    def __init__(self, expr=None):
        self.expr = expr if expr else READER_DESCRIPTION
        self.evaluator = {} # Compilet expressions
        self._loadExpr()

    def _loadExpr(self):
        for key, value in self.expr.items():
            self.evaluator[key] = re.compile(value)

    def getKey(self, string):
        result = self.evaluator['keys'].findall(string)
        if( len(result) == 0 ):
            return None
        else:
            return result[0]

    def getValue(self, string):
        return self.evaluator['values'].findall(string)

class Reader(object):

    def __init__(self, file_path, splitter=None):
        self.path = Path(file_path) if isValidPath(file_path) else None
        self.splitter = splitter if splitter else Splitter()
        self.info = {}

    def loadData(self):
        try:
            fp = open(self.path, 'r')
            current_key = None
            for line_data in fp:
                temp_key = self.splitter.getKey(line_data)
                if( temp_key ):
                    current_key = temp_key
                    self.info[current_key] = []
                else:
                    split_line = self.splitter.getValue(line_data)
                    if( len(split_line) > 0 ):
                        self.info[current_key].append( split_line )
                    else:
                        raise FileNotFoundError()
        finally:
            fp.close()

    def getData(self):
        return self.info
