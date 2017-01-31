class _ParserState(object):
    pass

_WHITESPACED_LINE_START = _ParserState()
_METACODE_TOKEN_START = _ParserState()
_METACODE = _ParserState()
_METACODE_TOKEN_END = _ParserState()
_REST_OF_LINE = _ParserState()

def parse(content):
    meta_count = 0
    line_number = 1
    state = _WHITESPACED_LINE_START
    for i, b in enumerate(content):
        if b == '\n':
            line_number += 1
            if state not in (_METACODE, _METACODE_TOKEN_END):
                state = _WHITESPACED_LINE_START

        else:
            if state == _WHITESPACED_LINE_START:
                if b == '<':
                    state = _METACODE_TOKEN_START

                elif b not in (' ', '\t', '\v', '\f', '\r'):
                    state = _REST_OF_LINE

            elif state == _METACODE_TOKEN_START:
                if b == '%':
                    state = _METACODE
                    meta_count += 1

                else:
                    state = _REST_OF_LINE

            elif state == _METACODE:
                if b == '%':
                    state = _METACODE_TOKEN_END

            elif state == _METACODE_TOKEN_END:
                if b == '>':
                    state = _REST_OF_LINE

                else:
                    state = _METACODE

    return meta_count
