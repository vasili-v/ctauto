import os.path
import collections
import yaml

from ctauto.exceptions import CTAutoInvalidDirectiveOrIdentifier, \
                              CTAutoUseDirectiveMissingFileName, \
                              CTAutoUseDirectiveInvalidFileName, \
                              CTAutoUseDirectiveTrailingTokens, \
                              CTAutoUseDirectiveDuplicateId, \
                              CTAutoUnknownIdentifier, \
                              CTAutoWrongPath, \
                              CTAutoWrongEntity

from ctauto.blocks import SimpleBlock
from ctauto.tokens import TextToken
from ctauto.symbols import UseFileName
from ctauto.parser import _METABLOCK_START
from ctauto.path import Path

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
        raise CTAutoUseDirectiveInvalidFileName(source, token.line, token=token)

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
    rest = []
    for index, block in control:
        token = block.tokens[0]
        if isinstance(token, TextToken):
            if token.text == _USE_DIRECTIVE:
                put_use_symbol(block, symbols, source)
            else:
                rest.append((index, block))
        else:
            raise CTAutoInvalidDirectiveOrIdentifier(source, token.line, token=token)

    return symbols, rest

def xpath_parser(control, symbols, source):
    items = collections.defaultdict(list)
    for index, block in control:
        token = block.tokens[0]
        if isinstance(token, TextToken):
            identifier = token.text
            try:
                symbol = symbols[identifier]
            except KeyError:
                raise CTAutoUnknownIdentifier(source, token.line, identifier=identifier)

            path = Path(token.line, symbol)
            path.parse(block.tokens[1:], source)
            items[identifier].append((index, path))
        else:
            raise CTAutoInvalidDirectiveOrIdentifier(source, token.line, token=token)

    return items

def replace(blocks, xpathitems, symbols, source):
    for identifier, items in xpathitems.iteritems():
        symbol = symbols[identifier]
        with open(symbol.name) as f:
            content = yaml.load(f)

        for index, path in items:
            entity = content
            for i, ref in enumerate(path.refs):
                try:
                    entity = ref(entity)
                except:
                    raise CTAutoWrongPath(source, ref.token.line, name=symbol.name,
                                          path=Path(path.line, path.root, path.refs[:i+1]))

            # PEP 285.6 Should bool inherit from int? => Yes. So check it for bool explicitly
            if isinstance(entity, bool) or not isinstance(entity, (basestring, int, long)):
                raise CTAutoWrongEntity(source, path.line, name=symbol.name,
                                        path=path, entity=type(entity).__name__)

            blocks[index] = SimpleBlock("%s" % entity)

    return blocks

def run(blocks, directory, source):
    control, result = _split(blocks)
    symbols, control = make_symbols(control, source)
    xpathitems = xpath_parser(control, symbols, source)
    return _rectify(replace(result, xpathitems, symbols, source))
