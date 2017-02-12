import unittest

from ctauto.blocks import Block, SimpleBlock, MetaBlock
from ctauto.tokens import SimpleTextToken

class TestBlock(unittest.TestCase):
    def test_create(self):
        block = Block("test")
        self.assertEqual(block.content, "test")

    def test_equal(self):
        first = Block("test")
        second = Block("test")

        self.assertTrue(first == second, "%s != %s" % (first, second))
        self.assertFalse(first != second, "%s == %s" % (first, second))

        first = Block("test")
        second = SimpleBlock("test")

        self.assertFalse(first == second, "%s == %s" % (first, second))

class TestMetaBlock(unittest.TestCase):
    def test_create(self):
        block = MetaBlock("test", [SimpleTextToken(1, "test")])
        self.assertEqual(block.content, "test")
        self.assertEqual(block.tokens, [SimpleTextToken(1, "test")])

test_suite = unittest.TestSuite([unittest.defaultTestLoader.loadTestsFromTestCase(TestBlock),
                                 unittest.defaultTestLoader.loadTestsFromTestCase(TestMetaBlock)])

if __name__ == '__main__':
    unittest.main()
