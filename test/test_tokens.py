import unittest

from ctauto.tokens import Token, TextToken, SimpleTextToken, QuotedTextToken, NumericToken

class TestToken(unittest.TestCase):
    def test_create(self):
        token = Token(1)
        self.assertEqual(token.line, 1)

    def test_equal(self):
        first = Token(1)
        second = Token(1)

        self.assertTrue(first == second, "%s != %s" % (first, second))
        self.assertFalse(first != second, "%s == %s" % (first, second))

        class Test(Token):
            pass

        first = Token(1)
        second = Test(1)

        self.assertFalse(first == second, "%s == %s" % (first, second))

        first = Token(1)
        second = Token(2)

        self.assertFalse(first == second, "%s == %s" % (first, second))

    def test_repr(self):
        token = Token(1)

        self.assertIn("Token", repr(token))
        self.assertIn("1", repr(token))

class TestTextToken(unittest.TestCase):
    def test_create(self):
        token = TextToken(1, "test")
        self.assertEqual(token.line, 1)
        self.assertEqual(token.text, "test")

    def test_equal(self):
        first = TextToken(1, "text")
        second = TextToken(1, "text")

        self.assertTrue(first == second, "%s != %s" % (first, second))
        self.assertFalse(first != second, "%s == %s" % (first, second))

        first = TextToken(1, "text")
        second = TextToken(1, "example")

        self.assertFalse(first == second, "%s == %s" % (first, second))

        first = SimpleTextToken(1, "text")
        second = QuotedTextToken(1, "text")

        self.assertFalse(first == second, "%s == %s" % (first, second))

    def test_repr(self):
        token = TextToken(1, "test")
        self.assertIn("test", repr(token))

class TestNumericToken(unittest.TestCase):
    def test_create(self):
        token = NumericToken(1, "0123")
        self.assertEqual(token.line, 1)
        self.assertEqual(token.digits, "0123")

    def test_equal(self):
        first = NumericToken(1, "0123")
        second = NumericToken(1, "0123")

        self.assertTrue(first == second, "%s != %s" % (first, second))
        self.assertFalse(first != second, "%s == %s" % (first, second))

        first = NumericToken(1, "0123")
        second = NumericToken(1, "3210")

        self.assertFalse(first == second, "%s == %s" % (first, second))

        first = NumericToken(1, "0123")
        second = QuotedTextToken(1, "0123")

        self.assertFalse(first == second, "%s == %s" % (first, second))

    def test_repr(self):
        token = NumericToken(1, "0123")
        self.assertIn("0123", repr(token))

test_suite = unittest.TestSuite([unittest.defaultTestLoader.loadTestsFromTestCase(TestToken),
                                 unittest.defaultTestLoader.loadTestsFromTestCase(TestTextToken),
                                 unittest.defaultTestLoader.loadTestsFromTestCase(TestNumericToken)])

if __name__ == '__main__':
    unittest.main()
