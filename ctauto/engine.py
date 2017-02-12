import os.path

from ctauto.blocks import SimpleBlock
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

def run(blocks, directory):
    control, result = _split(blocks)
    return _rectify(result)
