from ctauto.exceptions import CTAutoMissingEndOfMetablockError, \
                              CTAutoBrokenEndOfMetablockError, \
                              CTAutoInvalidMetablockError, \
                              CTAutoInvalidIdError, \
                              CTAutoInvalidNumberError, \
                              CTAutoMissingEndOfStringError, \
                              CTAutoInvalidStringError, \
                              CTAutoTrailingCharacterAfterQuotedText, \
                              CTAutoIncompleteEscapeSequence, \
                              CTAutoInvalidEscapeSequence

from ctauto.blocks import SimpleBlock, MetaBlock
from ctauto.tokens import SimpleTextToken, QuotedTextToken, NumericToken

class _EndOfFileCharacterType(object):
    pass

EndOfFileCharacter = _EndOfFileCharacterType()

class Parser(object):
    def parse(self, content, source):
        state = self.reset(content, source)
        for index, character in enumerate(content):
            state = state(index, character)

        state(len(content), EndOfFileCharacter)

        return self.finalize()

_METABLOCK_START = "<%"
_METABLOCK_END = "%>"
_END_OF_LINE = "\n"
_DOUBLE_QUOTE = "\""
_SLASH = "\\"
_WHITESPACES = (" ", "\t", "\v", "\f", "\r", _END_OF_LINE)
_ESCAPE_SEQUENCES = {"t": "\t", "v": "\v", "f": "\f", "r": "\r",
                     "n": _END_OF_LINE,
                     _DOUBLE_QUOTE: _DOUBLE_QUOTE,
                     _SLASH: _SLASH}

class TemplateParser(Parser):
    def reset(self, content, source):
        self.line = 1

        self.metablock_mark_index = 0

        self.source = source
        self.content = content
        self.start = 0

        self.blocks = []

        self.token = None
        self.tokens = []

        return self.check_metablock_start

    def finalize(self):
        return self.blocks

    def push_token(self):
        self.tokens.append(self.token)
        self.token = None

    def check_metablock_start(self, index, character):
        if self.metablock_mark_index == len(_METABLOCK_START):
            end = index - len(_METABLOCK_START)
            if end - self.start > 0:
                self.blocks.append(SimpleBlock(self.content[self.start:end]))

            self.start = index
            self.metablock_mark_index = 0
            return self.skip_white_spaces(index, character)

        if character is EndOfFileCharacter:
            if index - self.start > 0:
                self.blocks.append(SimpleBlock(self.content[self.start:index]))
            return

        if character == _METABLOCK_START[self.metablock_mark_index]:
            self.metablock_mark_index += 1
            return self.check_metablock_start

        if character == _END_OF_LINE:
            self.line += 1

        self.metablock_mark_index = 0
        return self.check_metablock_start

    def check_metablock_end(self, index, character):
        if self.metablock_mark_index == len(_METABLOCK_END):
            end = index - len(_METABLOCK_END)
            self.blocks.append(MetaBlock(self.content[self.start:end], self.tokens))
            self.tokens = []

            self.start = index
            self.metablock_mark_index = 0
            return self.check_metablock_start(index, character)

        if character is EndOfFileCharacter:
            raise CTAutoMissingEndOfMetablockError(self.source)

        if character == _METABLOCK_END[self.metablock_mark_index]:
            self.metablock_mark_index += 1
            return self.check_metablock_end

        sequence = "%s%s" % (_METABLOCK_END[:self.metablock_mark_index], character)
        raise CTAutoBrokenEndOfMetablockError(self.source, self.line, sequence=repr(sequence))

    def skip_white_spaces(self, index, character):
        if character is EndOfFileCharacter:
            raise CTAutoMissingEndOfMetablockError(self.source)

        if character in _WHITESPACES:
            if character == _END_OF_LINE:
                self.line += 1

            return self.skip_white_spaces

        if character == _METABLOCK_END[self.metablock_mark_index]:
            return self.check_metablock_end(index, character)

        if "A" <= character <= "Z" or "a" <= character <= "z" or character == "_":
            self.token = SimpleTextToken(self.line, character)
            return self.simple_text_token

        if "0" <= character <= "9":
            self.token = NumericToken(self.line, character)
            return self.numeric_token

        if character == _DOUBLE_QUOTE:
            self.token = QuotedTextToken(self.line)
            return self.quoted_text_token

        raise CTAutoInvalidMetablockError(self.source, self.line, character=repr(character))

    def simple_text_token(self, index, character):
        if character is EndOfFileCharacter:
            raise CTAutoMissingEndOfMetablockError(self.source)

        if character in _WHITESPACES:
            self.push_token()

            return self.skip_white_spaces(index, character)

        if character == _METABLOCK_END[self.metablock_mark_index]:
            self.push_token()

            return self.check_metablock_end(index, character)

        if "0" <= character <= "9" or "A" <= character <= "Z" or "a" <= character <= "z" or character == "_":
            self.token.text += character
            return self.simple_text_token

        sequence = "%s%s" % (self.token.text, character)
        raise CTAutoInvalidIdError(self.source, self.line, sequence=repr(sequence))

    def quoted_text_token(self, index, character):
        if character is EndOfFileCharacter:
            raise CTAutoMissingEndOfStringError(self.source)

        if character == _END_OF_LINE:
            raise CTAutoInvalidStringError(self.source, self.line)

        if character == _DOUBLE_QUOTE:
            self.push_token()

            return self.skip_white_spaces_after_quoted_text

        if character == _SLASH:
            return self.quoted_text_token_escape_sequence

        self.token.text += character
        return self.quoted_text_token

    def quoted_text_token_escape_sequence(self, index, character):
        if character is EndOfFileCharacter:
            raise CTAutoIncompleteEscapeSequence(self.source)

        if character == _END_OF_LINE:
            raise CTAutoInvalidEscapeSequence(self.source, self.line)

        self.token.text += _ESCAPE_SEQUENCES.get(character, "\\%s" % character)
        return self.quoted_text_token

    def skip_white_spaces_after_quoted_text(self, index, character):
        if character is EndOfFileCharacter:
            raise CTAutoMissingEndOfMetablockError(self.source)

        if character in _WHITESPACES:
            return self.skip_white_spaces(index, character)

        if character == _METABLOCK_END[self.metablock_mark_index]:
            return self.check_metablock_end(index, character)

        raise CTAutoTrailingCharacterAfterQuotedText(self.source, self.line, character=repr(character))

    def numeric_token(self, index, character):
        if character is EndOfFileCharacter:
            raise CTAutoMissingEndOfMetablockError(self.source)

        if character in _WHITESPACES:
            self.push_token()

            return self.skip_white_spaces(index, character)

        if character == _METABLOCK_END[self.metablock_mark_index]:
            self.push_token()

            return self.check_metablock_end(index, character)

        if "0" <= character <= "9":
            self.token.digits += character
            return self.numeric_token

        sequence = "%s%s" % (self.token.digits, character)
        raise CTAutoInvalidNumberError(self.source, self.line, sequence=repr(sequence))
