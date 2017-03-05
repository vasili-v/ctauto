import unittest

from ctauto.exceptions import CTAutoInvalidDirective, \
                              CTAutoUseDirectiveMissingFileName, \
                              CTAutoUseDirectiveInvalidFileName, \
                              CTAutoUseDirectiveTrailingTokens, \
                              CTAutoUseDirectiveDuplicateId

from ctauto.blocks import SimpleBlock, MetaBlock
from ctauto.tokens import SimpleTextToken, QuotedTextToken, NumericToken, LeftSquareBracketToken
from ctauto.symbols import UseFileName

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

        result = list(ctauto.engine.run(blocks, None, "template"))
        self.assertEqual(result, [block1, block3, SimpleBlock("<%"), block5])

    def test_make_symbols(self):
        use = MetaBlock("use \"template.yaml\"", [SimpleTextToken(2, "use"), QuotedTextToken(2, "template.yaml")])

        symbols = ctauto.engine.make_symbols([(1, use)], "template")
        self.assertEqual(symbols, {"template": UseFileName(2, "template", "template.yaml")})

    def test_make_symbols_invalid_directive(self):
        bracket = LeftSquareBracketToken(2)
        use = MetaBlock(". use \"template.yaml\"",
                        [bracket, SimpleTextToken(2, "use"), QuotedTextToken(2, "template.yaml")])

        with self.assertRaises(CTAutoInvalidDirective) as ctx:
            ctauto.engine.make_symbols([(1, use)], "template")

        self.assertIn(bracket.content(), str(ctx.exception))

    def test_make_symbols_use_miss_file_name(self):
        use = MetaBlock("use", [SimpleTextToken(2, "use")])
        with self.assertRaises(CTAutoUseDirectiveMissingFileName):
            ctauto.engine.make_symbols([(1, use)], "template")

    def test_make_symbols_use_invalid_file_name(self):
        use = MetaBlock("use 123", [SimpleTextToken(2, "use"), NumericToken(2, "123")])
        with self.assertRaises(CTAutoUseDirectiveInvalidFileName):
            ctauto.engine.make_symbols([(1, use)], "template")

        use = MetaBlock("use \"\"", [SimpleTextToken(2, "use"), QuotedTextToken(2, "")])
        with self.assertRaises(CTAutoUseDirectiveInvalidFileName):
            ctauto.engine.make_symbols([(1, use)], "template")

    def test_make_symbols_use_duplicate_identifier(self):
        first = MetaBlock("use \"template.yaml\"", [SimpleTextToken(2, "use"), QuotedTextToken(2, "template.yaml")])
        second = MetaBlock("use \"template.yaml\"", [SimpleTextToken(3, "use"), QuotedTextToken(3, "template.yaml")])
        with self.assertRaises(CTAutoUseDirectiveDuplicateId):
            ctauto.engine.make_symbols([(1, first), (2, second)], "template")

    def test_make_symbols_use_traling_tokens(self):
        use = MetaBlock("use \"template.yaml\" test [ test 123",
                        [SimpleTextToken(2, "use"),
                         QuotedTextToken(2, "template.yaml"),
                         SimpleTextToken(2, "test"),
                         LeftSquareBracketToken(2),
                         SimpleTextToken(2, "test"),
                         NumericToken(2, "123")])

        with self.assertRaises(CTAutoUseDirectiveTrailingTokens):
            ctauto.engine.make_symbols([(1, use)], "template")

test_suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestEngine)

if __name__ == '__main__':
    unittest.main()
