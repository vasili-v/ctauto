class CTAutoError(Exception):
    def __init__(self, **kwargs):
        super(CTAutoError, self).__init__(self.template % kwargs)

class CTAutoSourceError(CTAutoError):
    def __init__(*args, **kwargs):
        self, source = args
        self.template = "%s: %s" % (source, self.template)
        super(CTAutoSourceError, self).__init__(**kwargs)

class CTAutoSourceLineError(CTAutoError):
    def __init__(*args, **kwargs):
        self, source, line = args
        self.template = "%s:%d: %s" % (source, line, self.template)
        super(CTAutoSourceLineError, self).__init__(**kwargs)

class CTAutoMissingEndOfMetablockError(CTAutoSourceError):
    template = "missing end of metablock"

class CTAutoBrokenEndOfMetablockError(CTAutoSourceLineError):
    template = "expected end of metablock got %(sequence)s"

class CTAutoInvalidMetablockError(CTAutoSourceLineError):
    template = "expected whitespace, end of metablock, identifier, number or string but got %(character)s"

class CTAutoInvalidIdError(CTAutoSourceLineError):
    template = "expected identifier but got %(sequence)s"

class CTAutoMissingEndOfStringError(CTAutoSourceError):
    template = "missing end of string"

class CTAutoInvalidStringError(CTAutoSourceLineError):
    template = "new line isn't allowed inside string literal use \"\\n\" instead"

class CTAutoIncompleteEscapeSequence(CTAutoSourceError):
    template = "expected escape sequence but got end of file"

class CTAutoInvalidEscapeSequence(CTAutoSourceLineError):
    template = "expected escape sequence but got end of line"

class CTAutoTrailingCharacterAfterQuotedText(CTAutoSourceLineError):
    template = "expected whitespace or end of metablock after string but got %(character)s"

class CTAutoInvalidNumberError(CTAutoSourceLineError):
    template = "expected number but got %(sequence)s"
