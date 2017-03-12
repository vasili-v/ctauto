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

class CTAutoInvalidDirectiveOrIdentifier(CTAutoSourceLineError):
    template = "expected directive or identifier but got %(token)s"

class CTAutoUseDirectiveMissingFileName(CTAutoSourceLineError):
    template = "missing file name for \"use\" directive"

class CTAutoUseDirectiveInvalidFileName(CTAutoSourceLineError):
    template = "expected file name but got %(token)s"

class CTAutoUseDirectiveTrailingTokens(CTAutoSourceLineError):
    template = "don't expect tokens after file name"

class CTAutoUseDirectiveDuplicateId(CTAutoSourceLineError):
    template = "duplicate identifier %(identifier)s"

class CTAutoUnknownIdentifier(CTAutoSourceLineError):
    template = "unknown identifier %(identifier)s"

class CTAutoPathInvalidSeparator(CTAutoSourceLineError):
    template = "expected dot or bracket after %(path)s but got %(token)s"

class CTAutoPathMissingObjectFieldName(CTAutoSourceLineError):
    template = "missing object field name in path %(path)s"

class CTAutoPathInvalidObjectFieldName(CTAutoSourceLineError):
    template = "expected text token after %(path)s but got %(token)s"

class CTAutoPathMissingArrayItemIndex(CTAutoSourceLineError):
    template = "missing array item index in path %(path)s"

class CTAutoPathInvalidArrayItemIndex(CTAutoSourceLineError):
    template = "expected numeric token after %(path)s but got %(token)s"

class CTAutoPathMissingRightSquareBracket(CTAutoSourceLineError):
    template = "missing bracket after %(path)s"

class CTAutoPathInvalidRightSquareBracket(CTAutoSourceLineError):
    template = "expected bracket after %(path)s but got %(token)s"
