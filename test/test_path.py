import unittest

from ctauto.exceptions import CTAutoPathInvalidSeparator, \
                              CTAutoPathMissingObjectFieldName, \
                              CTAutoPathInvalidObjectFieldName, \
                              CTAutoPathMissingArrayItemIndex, \
                              CTAutoPathInvalidArrayItemIndex, \
                              CTAutoPathMissingRightSquareBracket, \
                              CTAutoPathInvalidRightSquareBracket

from ctauto.symbols import UseFileName
from ctauto.tokens import SimpleTextToken, NumericToken, DotToken, LeftSquareBracketToken, RightSquareBracketToken
from ctauto.path import Path, Ref, ObjectFieldRef, ArrayItemRef

class TestPath(unittest.TestCase):
    def test_create(self):
        root = UseFileName(2, "template", "template.yaml")
        refs = [ObjectFieldRef(SimpleTextToken(1, "test")), ArrayItemRef(NumericToken(1, "1"), True)]
        path = Path(root, refs)
        self.assertEqual(path.root, root)
        self.assertEqual(path.refs, refs)

    def test_equal(self):
        root1 = UseFileName(1, "test", "test.yaml")
        root2 = UseFileName(2, "example", "example.yaml")

        refs1 = [ObjectFieldRef(SimpleTextToken(3, "test")), ArrayItemRef(NumericToken(3, "3"), True)]
        refs2 = [ObjectFieldRef(SimpleTextToken(4, "example")), ArrayItemRef(NumericToken(4, "4"), True)]
        refs3 = [ObjectFieldRef(SimpleTextToken(5, "example"))]

        first = Path(root1, refs1)
        second = Path(root1, refs1)

        self.assertTrue(first == second, "%s != %s" % (repr(first), repr(second)))
        self.assertFalse(first != second, "%s == %s" % (repr(first), repr(second)))

        second = Path(root2, refs1)
        self.assertFalse(first == second, "%s == %s" % (repr(first), repr(second)))

        second = Path(root1, refs2)
        self.assertFalse(first == second, "%s == %s" % (repr(first), repr(second)))

        second = Path(root1, refs3)
        self.assertFalse(first == second, "%s == %s" % (repr(first), repr(second)))

    def test_repr(self):
        root = UseFileName(1, "test", "test.yaml")
        ref = ObjectFieldRef(SimpleTextToken(3, "test"))
        path = Path(root, [ref])

        self.assertIn("Path", repr(path))
        self.assertIn(repr(root), repr(path))
        self.assertIn(str(ref), repr(path))

    def test_str(self):
        root = UseFileName(1, "test", "test.yaml")
        ref = ObjectFieldRef(SimpleTextToken(3, "test"))

        path = Path(root)
        self.assertIn(root.identifier, str(path))

        path = Path(root, [ref])
        self.assertIn(root.identifier, str(path))
        self.assertIn(str(ref), str(path))

    def test_parse(self):
        root = UseFileName(1, "test", "test.yaml")
        text = SimpleTextToken(1, "test")
        number = NumericToken(1, "123")
        tokens = [DotToken(1), text, LeftSquareBracketToken(1), number, RightSquareBracketToken(1)]

        path = Path(root)
        path.parse(tokens, "template")

        self.assertEqual(path.refs, [ObjectFieldRef(text), ArrayItemRef(number, True)])

    def test_parse_invalid_separator(self):
        path = Path(UseFileName(1, "test", "test.yaml"))
        text = SimpleTextToken(1, "test")

        with self.assertRaises(CTAutoPathInvalidSeparator) as ctx:
            path.parse([text], "template")

        self.assertIn(str(path), str(ctx.exception))
        self.assertIn(str(text), str(ctx.exception))

    def test_parse_missing_name(self):
        path = Path(UseFileName(1, "test", "test.yaml"))
        with self.assertRaises(CTAutoPathMissingObjectFieldName) as ctx:
            path.parse([DotToken(1)], "template")

        self.assertIn(str(path), str(ctx.exception))

    def test_parse_invalid_name(self):
        path = Path(UseFileName(1, "test", "test.yaml"))
        dot = DotToken(1)
        with self.assertRaises(CTAutoPathInvalidObjectFieldName) as ctx:
            path.parse([dot, dot], "template")

        self.assertIn(str(path), str(ctx.exception))
        self.assertIn(str(dot), str(ctx.exception))

    def test_parse_missing_index(self):
        path = Path(UseFileName(1, "test", "test.yaml"))
        with self.assertRaises(CTAutoPathMissingArrayItemIndex) as ctx:
            path.parse([LeftSquareBracketToken(1)], "template")

        self.assertIn(str(path), str(ctx.exception))

    def test_parse_invalid_index(self):
        path = Path(UseFileName(1, "test", "test.yaml"))
        bracket = LeftSquareBracketToken(1)
        with self.assertRaises(CTAutoPathInvalidArrayItemIndex) as ctx:
            path.parse([bracket, bracket], "template")

        self.assertIn(str(path), str(ctx.exception))
        self.assertIn(str(bracket), str(ctx.exception))

    def test_parse_missing_bracket(self):
        path = Path(UseFileName(1, "test", "test.yaml"))
        with self.assertRaises(CTAutoPathMissingRightSquareBracket) as ctx:
            path.parse([LeftSquareBracketToken(1), NumericToken(1, "1")], "template")

        self.assertIn(str(path), str(ctx.exception))

    def test_parse_invalid_bracket(self):
        path = Path(UseFileName(1, "test", "test.yaml"))
        bracket = LeftSquareBracketToken(1)
        with self.assertRaises(CTAutoPathInvalidRightSquareBracket) as ctx:
            path.parse([bracket, NumericToken(1, "1"), bracket], "template")

        self.assertIn(str(path), str(ctx.exception))
        self.assertIn(str(bracket), str(ctx.exception))

class TestRef(unittest.TestCase):
    def test_create(self):
        token = SimpleTextToken(1, "test")
        ref = Ref(token)
        self.assertEqual(ref.token, token)

    def test_equal(self):
        token1 = SimpleTextToken(1, "test")
        token2 = SimpleTextToken(2, "example")

        first = Ref(token1)
        second = Ref(token1)

        self.assertTrue(first == second, "%s != %s" % (repr(first), repr(second)))
        self.assertFalse(first != second, "%s == %s" % (repr(first), repr(second)))

        class Test(Ref):
            pass

        second = Test(token1)
        self.assertTrue(first != second, "%s == %s" % (repr(first), repr(second)))

        second = Ref(token2)
        self.assertTrue(first != second, "%s == %s" % (repr(first), repr(second)))

    def test_repr(self):
        token = SimpleTextToken(1, "test")
        ref = Ref(token)
        self.assertIn("Ref", repr(ref))
        self.assertIn(repr(token), repr(ref))

class TestObjectFieldRef(unittest.TestCase):
    def test_create(self):
        token = SimpleTextToken(1, "test")
        ref = ObjectFieldRef(token)
        self.assertEqual(ref.token, token)

    def test_str(self):
        token = SimpleTextToken(1, "test")

        ref = ObjectFieldRef(token)
        content = str(ref)
        self.assertIn(token.text, content)

        ref = ObjectFieldRef(None)
        content = str(ref)
        self.assertEqual(content, ".")

class TestArrayItemRef(unittest.TestCase):
    def test_create(self):
        token = NumericToken(1, "1")
        ref = ArrayItemRef(token, True)
        self.assertEqual(ref.token, token)
        self.assertTrue(ref.complete)

    def test_equal(self):
        token1 = NumericToken(1, "1")
        token2 = NumericToken(2, "2")

        first = ArrayItemRef(token1, True)
        second = ArrayItemRef(token1, True)

        self.assertTrue(first == second, "%s != %s" % (repr(first), repr(second)))
        self.assertFalse(first != second, "%s == %s" % (repr(first), repr(second)))

        second = ArrayItemRef(token2, True)
        self.assertFalse(first == second, "%s == %s" % (repr(first), repr(second)))

        second = ArrayItemRef(token1, False)
        self.assertFalse(first == second, "%s == %s" % (repr(first), repr(second)))

    def test_str(self):
        token = NumericToken(1, "1")

        ref = ArrayItemRef(None)
        content = str(ref)
        self.assertEqual(content, "[")

        ref = ArrayItemRef(token)
        content = str(ref)
        self.assertIn(token.digits, content)
        self.assertNotIn("]", content)

        ref = ArrayItemRef(token, True)
        content = str(ref)
        self.assertIn(token.digits, content)
        self.assertIn("]", content)

test_suite = unittest.TestSuite([unittest.defaultTestLoader.loadTestsFromTestCase(TestPath),
                                 unittest.defaultTestLoader.loadTestsFromTestCase(TestRef),
                                 unittest.defaultTestLoader.loadTestsFromTestCase(TestObjectFieldRef),
                                 unittest.defaultTestLoader.loadTestsFromTestCase(TestArrayItemRef)])

if __name__ == '__main__':
    unittest.main()
