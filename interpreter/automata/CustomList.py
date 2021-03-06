class CustomList(list):
    def __init__(self, list):
        super().__init__(list)

    def __contains__(self, element):
        error_msg = "Value=%r, not in %r" %(element, self)
        if( not isinstance(element, list) ):
            if( list.__contains__(self, element) ):
                return True
            else:
                raise LookupError(error_msg)
        elif( isinstance(element, list) ):
            for item in element:
                if( not list.__contains__(self, item) ):
                    raise LookupError(error_msg)
            return True

    def append(self, element):
        if( not list.__contains__(self, element) ):
            list.append(self, element)
        else:
            raise RepeatedValueException("Value=%r, already in list." % element)

    def intersection(self, other):
        return [element for element in self if element in other]

class RepeatedValueException(Exception):
    def __init__(self, message):
        self.message = message
