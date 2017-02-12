class Block(object):
    def __init__(self, content):
        self.content = content

    def __eq__(self, other):
        return type(self) is type(other) and self.content == other.content

    def __ne__(self, other):
        return not self.__eq__(other)

class SimpleBlock(Block):
    pass

class MetaBlock(Block):
    def __init__(self, content, tokens):
        super(MetaBlock, self).__init__(content)
        self.tokens = tokens
