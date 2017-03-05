class Symbol(object):
    def __init__(self, line, identifier):
        self.line = line
        self.identifier = identifier

    def __eq__(self, other):
        return type(self) is type(other) and \
               self.line == other.line and self.identifier == other.identifier

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "<%s(line=%s, id=%s)>" % (type(self).__name__, repr(self.line), repr(self.identifier))

class UseFileName(Symbol):
    def __init__(self, line, identifier, name):
        super(UseFileName, self).__init__(line, identifier)
        self.name = name

    def __eq__(self, other):
        return super(UseFileName, self).__eq__(other) and self.name == other.name

    def __repr__(self):
        return "<%s(line=%s, id=%s, name=%s)>" % \
               (type(self).__name__, repr(self.line), repr(self.identifier), repr(self.name))
