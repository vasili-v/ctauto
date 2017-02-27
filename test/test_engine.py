import unittest

from ctauto.blocks import SimpleBlock, MetaBlock
from ctauto.tokens import SimpleTextToken, NumericToken

import ctauto.engine

class TestEngine(unittest.TestCase):
    def test__split(self):
        block1 = SimpleBlock("part 1")
        block2 = MetaBlock("part 2", [SimpleTextToken(2, "part"), NumericToken(2, "2")])
        block3 = SimpleBlock("part 3")
        block4 = MetaBlock("", [])
        block5 = SimpleBlock("part 5")

        blocks = [block1, block2, block3, block4, block5]

        control, result = ctauto.engine._split(blocks)
        self.assertEqual(control, [(1, block2)])
        self.assertEqual(result, [block1, None, block3, SimpleBlock("<%"), block5])

    def test__rectify(self):
        block1 = SimpleBlock("part 1")
        block3 = SimpleBlock("part 3")
        block4 = SimpleBlock("<%")

        blocks = [block1, None, block3, block4]

        result = list(ctauto.engine._rectify(blocks))
        self.assertEqual(result, [block1, block3, block4])

    def test_run(self):
        block1 = SimpleBlock("part 1")
        block2 = MetaBlock("part 2", [SimpleTextToken(2, "part"), NumericToken(2, "2")])
        block3 = SimpleBlock("part 3")
        block4 = MetaBlock("", [])
        block5 = SimpleBlock("part 5")

        blocks = [block1, block2, block3, block4, block5]

        result = list(ctauto.engine.run(blocks, None))
        self.assertEqual(result, [block1, block3, SimpleBlock("<%"), block5])

    def test_make_symbols(self):
        symbols = ctauto.engine.make_symbols(None)
        self.assertEqual(symbols, {})

test_suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestEngine)

if __name__ == '__main__':
    unittest.main()
