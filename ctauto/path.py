from ctauto.exceptions import CTAutoPathInvalidSeparator, \
                              CTAutoPathMissingObjectFieldName, \
                              CTAutoPathInvalidObjectFieldName, \
                              CTAutoPathMissingArrayItemIndex, \
                              CTAutoPathInvalidArrayItemIndex, \
                              CTAutoPathMissingRightSquareBracket, \
                              CTAutoPathInvalidRightSquareBracket

from ctauto.tokens import TextToken, NumericToken, DotToken, LeftSquareBracketToken, RightSquareBracketToken

class Path(object):
    def __init__(self, line, root, refs=None):
        self.line = line
        self.root = root
        self.refs = refs if refs is not None else []

    def __eq__(self, other):
        if self.root != other.root or len(self.refs) != len(other.refs):
            return False

        for i, ref in enumerate(self.refs):
            if ref != other.refs[i]:
                return False

        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        refs = ", ".join(["\"%s\"" % ref for ref in self.refs])
        return "<%s(line=%s, root=%s, refs=[%s])>" % (type(self).__name__, self.line, repr(self.root), refs)

    def __str__(self):
        if self.refs:
            return "%s%s" % (self.root.identifier, "".join([str(ref) for ref in self.refs]))

        return self.root.identifier

    def parse(self, tokens, source):
        iterator = iter(tokens)
        for token in iterator:
            if isinstance(token, DotToken):
                try:
                    name = iterator.next()
                except StopIteration:
                    raise CTAutoPathMissingObjectFieldName(source, token.line, path=self)

                if not isinstance(name, TextToken):
                    self.refs.append(ObjectFieldRef(None))
                    raise CTAutoPathInvalidObjectFieldName(source, token.line, path=self, token=name)

                self.refs.append(ObjectFieldRef(name))

            elif isinstance(token, LeftSquareBracketToken):
                try:
                    index = iterator.next()
                except StopIteration:
                    raise CTAutoPathMissingArrayItemIndex(source, token.line, path=self)

                if not isinstance(index, NumericToken):
                    raise CTAutoPathInvalidArrayItemIndex(source, token.line, path=self, token=index)

                self.refs.append(ArrayItemRef(index))

                try:
                    bracket = iterator.next()
                except StopIteration:
                    raise CTAutoPathMissingRightSquareBracket(source, index.line, path=self)

                if not isinstance(bracket, RightSquareBracketToken):
                    raise CTAutoPathInvalidRightSquareBracket(source, bracket.line, path=self, token=bracket)

                self.refs[-1].complete = True

            else:
                raise CTAutoPathInvalidSeparator(source, token.line, path=self, token=token)

class Ref(object):
    def __init__(self, token):
        self.token = token

    def __eq__(self, other):
        return type(self) is type(other) and self.token == other.token

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "<%s(token=%s)>" % (type(self).__name__, repr(self.token))

class ObjectFieldRef(Ref):
    def __init__(self, token):
        super(ObjectFieldRef, self).__init__(token)
        if self.token is not None:
            self.name = self.token.text

    def __str__(self):
        if self.token is None:
            return "."

        return ".%s" % self.name

    def __call__(self, content):
        return content[self.token.text]

class ArrayItemRef(Ref):
    def __init__(self, token, complete=False):
        super(ArrayItemRef, self).__init__(token)
        if self.token is not None:
            self.index = int(self.token.digits)

        self.complete = complete

    def __eq__(self, other):
        return super(ArrayItemRef, self).__eq__(other) and self.complete == other.complete

    def __str__(self):
        if self.token is None:
            return "["

        if not self.complete:
            return "[%s" % self.index

        return "[%s]" % self.index

    def __call__(self, content):
        return content[self.index]
