import unittest

from ctauto.symbols import Symbol, UseFileName

class TestSymbol(unittest.TestCase):
    def test_create(self):
        symbol = Symbol(1, "s")
        self.assertEqual(symbol.line, 1)
        self.assertEqual(symbol.identifier, "s")

    def test_equal(self):
        first = Symbol(1, "s")
        second = Symbol(1, "s")

        self.assertTrue(first == second, "%s != %s" % (first, second))
        self.assertFalse(first != second, "%s == %s" % (first, second))

        class Test(Symbol):
            pass

        first = Symbol(1, "s")
        second = Test(1, "s")

        self.assertFalse(first == second, "%s == %s" % (first, second))

        first = Symbol(1, "s")
        second = Symbol(2, "s")

        self.assertFalse(first == second, "%s == %s" % (first, second))

        first = Symbol(1, "s")
        second = Symbol(1, "t")

        self.assertFalse(first == second, "%s == %s" % (first, second))

    def test_repr(self):
        symbol = Symbol(1, "test")

        self.assertIn("Symbol", repr(symbol))
        self.assertIn("1", repr(symbol))
        self.assertIn("test", repr(symbol))

class TestUseFileName(unittest.TestCase):
    def test_create(self):
        use = UseFileName(1, "test", "template.yaml")
        self.assertEqual(use.line, 1)
        self.assertEqual(use.identifier, "test")
        self.assertEqual(use.name, "template.yaml")

    def test_equal(self):
        first = UseFileName(1, "test", "test.test")
        second = UseFileName(1, "test", "test.test")

        self.assertTrue(first == second, "%s != %s" % (first, second))
        self.assertFalse(first != second, "%s == %s" % (first, second))

        first = UseFileName(1, "test", "template.yaml")
        second = UseFileName(1, "test", "example.yaml")

        self.assertFalse(first == second, "%s == %s" % (first, second))

    def test_repr(self):
        use = UseFileName(1, "test", "template.yaml")
        self.assertIn("template.yaml", repr(use))

test_suite = unittest.TestSuite([unittest.defaultTestLoader.loadTestsFromTestCase(TestSymbol),
                                 unittest.defaultTestLoader.loadTestsFromTestCase(TestUseFileName)])

if __name__ == '__main__':
    unittest.main()
