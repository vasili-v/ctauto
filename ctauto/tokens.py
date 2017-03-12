class Token(object):
    def __init__(self, line):
        self.line = line

    def __eq__(self, other):
        return type(self) is type(other) and self.line == other.line

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "<%s(line=%s)>" % (type(self).__name__, repr(self.line))

class TextToken(Token):
    def __init__(self, line, character=""):
        super(TextToken, self).__init__(line)
        self.text = character

    def __eq__(self, other):
        return super(TextToken, self).__eq__(other) and self.text == other.text

    def __repr__(self):
        return "<%s(line=%s, text=%s)>" % (type(self).__name__, repr(self.line), repr(self.text))

    def __str__(self):
        return '"%s"' % self.text

class SimpleTextToken(TextToken):
    pass

class QuotedTextToken(TextToken):
    pass

class NumericToken(Token):
    def __init__(self, line, digit):
        super(NumericToken, self).__init__(line)
        self.digits = digit

    def __eq__(self, other):
        return super(NumericToken, self).__eq__(other) and self.digits == other.digits

    def __repr__(self):
        return "<%s(line=%s, digits=%s>" % (type(self).__name__, repr(self.line), repr(self.digits))

    def __str__(self):
        return "%s" % self.digits

class DotToken(Token):
    def __str__(self):
        return '"."'

class LeftSquareBracketToken(Token):
    def __str__(self):
        return '"["'

class RightSquareBracketToken(Token):
    def __str__(self):
        return '"]"'
