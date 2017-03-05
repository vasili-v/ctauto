import os.path

from ctauto.exceptions import CTAutoInvalidDirective, \
                              CTAutoUseDirectiveMissingFileName, \
                              CTAutoUseDirectiveInvalidFileName, \
                              CTAutoUseDirectiveTrailingTokens, \
                              CTAutoUseDirectiveDuplicateId

from ctauto.blocks import SimpleBlock
from ctauto.tokens import TextToken
from ctauto.symbols import UseFileName
from ctauto.parser import _METABLOCK_START

def _split(blocks):
    control = []
    result = []
    for index, block in enumerate(blocks):
        if isinstance(block, SimpleBlock):
            result.append(block)

        elif block.tokens:
            result.append(None)
            control.append((index, block))

        else:
            result.append(SimpleBlock(_METABLOCK_START))

    return control, result

def _rectify(blocks):
    for block in blocks:
        if block is None:
            continue

        yield block

_USE_DIRECTIVE = "use"

def put_use_symbol(block, symbols, source):
    if len(block.tokens) <= 1:
        raise CTAutoUseDirectiveMissingFileName(source, block.tokens[0].line)

    token = block.tokens[1]
    if not isinstance(token, TextToken) or not token.text:
        raise CTAutoUseDirectiveInvalidFileName(source, token.line, token=token.content())

    name = token.text
    identifier = os.path.splitext(os.path.basename(name))[0]
    if identifier in symbols:
        raise CTAutoUseDirectiveDuplicateId(source, token.line,
                                            identifier=identifier, previous=symbols[identifier].line)

    if len(block.tokens) > 2:
        token = block.tokens[2]
        raise CTAutoUseDirectiveTrailingTokens(source, token.line, count=len(block.tokens)-2)

    symbols[identifier] = UseFileName(token.line, identifier, name)

def make_symbols(control, source):
    symbols = {}
    for index, block in control:
        token = block.tokens[0]
        if isinstance(token, TextToken):
            if token.text == _USE_DIRECTIVE:
                put_use_symbol(block, symbols, source)
        else:
            raise CTAutoInvalidDirective(source, token.line, token=token.content())

    return symbols

def run(blocks, directory, source):
    control, result = _split(blocks)
    symbols = make_symbols(control, source)
    return _rectify(result)
