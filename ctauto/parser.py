from ctauto.exceptions import CTAutoMissingEndOfMetablockError
from ctauto.blocks import Block, MetaBlock

class _EndOfFileCharacterType(object):
    pass

EndOfFileCharacter = _EndOfFileCharacterType()

class Parser(object):
    def parse(self, content, source):
        state = self.reset(content, source)
        for index, character in enumerate(content):
            state = state(index, character)

        state(len(content), EndOfFileCharacter)

_METABLOCK_START = "<%"
_METABLOCK_END = "%>"

class TemplateParser(Parser):
    def reset(self, content, source):
        self.metablock_mark_index = 0

        self.source = source
        self.content = content
        self.start = 0

        self.blocks = []

        return self.check_metablock_start

    def check_metablock_start(self, index, character):
        if self.metablock_mark_index == len(_METABLOCK_START):
            end = index - len(_METABLOCK_START)
            if end - self.start > 0:
                self.blocks.append(Block(self.content[self.start:end]))

            self.start = index
            self.metablock_mark_index = 0
            return self.check_metablock_end(index, character)

        if character is EndOfFileCharacter:
            if index - self.start > 0:
                self.blocks.append(Block(self.content[self.start:index]))
            return

        if character == _METABLOCK_START[self.metablock_mark_index]:
            self.metablock_mark_index += 1
            return self.check_metablock_start

        self.metablock_mark_index = 0
        return self.check_metablock_start

    def check_metablock_end(self, index, character):
        if self.metablock_mark_index == len(_METABLOCK_END):
            end = index - len(_METABLOCK_END)
            self.blocks.append(MetaBlock(self.content[self.start:end]))

            self.start = index
            self.metablock_mark_index = 0
            return self.check_metablock_start(index, character)

        if character is EndOfFileCharacter:
            raise CTAutoMissingEndOfMetablockError(self.source)

        if character == _METABLOCK_END[self.metablock_mark_index]:
            self.metablock_mark_index += 1
            return self.check_metablock_end

        self.metablock_mark_index = 0
        return self.check_metablock_end
