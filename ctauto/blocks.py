class Block(object):
    def __init__(self, content):
        self.content = content

class MetaBlock(Block):
    def __init__(self, content, tokens):
        super(MetaBlock, self).__init__(content)
        self.tokens = tokens
