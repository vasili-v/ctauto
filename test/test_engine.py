import unittest

from ctauto.exceptions import CTAutoInvalidDirectiveOrIdentifier, \
                              CTAutoUseDirectiveMissingFileName, \
                              CTAutoUseDirectiveInvalidFileName, \
                              CTAutoUseDirectiveTrailingTokens, \
                              CTAutoUseDirectiveDuplicateId, \
                              CTAutoUnknownIdentifier

from ctauto.blocks import SimpleBlock, MetaBlock
from ctauto.tokens import SimpleTextToken, \
                          QuotedTextToken, \
                          NumericToken, \
                          DotToken, \
                          LeftSquareBracketToken, \
                          RightSquareBracketToken

from ctauto.symbols import UseFileName
from ctauto.path import Path, ObjectFieldRef, ArrayItemRef

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
        block2 = MetaBlock("use \"part.yaml\"", [SimpleTextToken(2, "use"), QuotedTextToken(2, "part.yaml")])
        block3 = MetaBlock("part [ 3 ]", [SimpleTextToken(3, "part"),
                                          LeftSquareBracketToken(3),
                                          NumericToken(3, "3"),
                                          RightSquareBracketToken(3)])
        block4 = SimpleBlock("part 4")
        block5 = MetaBlock("", [])
        block6 = SimpleBlock("part 6")

        blocks = [block1, block2, block3, block4, block5, block6]

        result = list(ctauto.engine.run(blocks, None, "template"))
        self.assertEqual(result, [block1, block4, SimpleBlock("<%"), block6])

    def test_make_symbols(self):
        use = MetaBlock("use \"template.yaml\"", [SimpleTextToken(2, "use"), QuotedTextToken(2, "template.yaml")])
        path1 = MetaBlock("template.test", [SimpleTextToken(3, "template"), DotToken(3), SimpleTextToken(3, "test")])
        path2 = MetaBlock("template.example[4]", [SimpleTextToken(4, "template"),
                                                  DotToken(4),
                                                  SimpleTextToken(4, "example"),
                                                  LeftSquareBracketToken(4),
                                                  NumericToken(4, "4"),
                                                  RightSquareBracketToken(4)])

        symbols, rest = ctauto.engine.make_symbols([(1, use), (2, path1), (3, path2)], "template")
        self.assertEqual(symbols, {"template": UseFileName(2, "template", "template.yaml")})
        self.assertEqual(rest, [(2, path1), (3, path2)])

    def test_make_symbols_invalid_directive(self):
        bracket = LeftSquareBracketToken(2)
        use = MetaBlock(". use \"template.yaml\"",
                        [bracket, SimpleTextToken(2, "use"), QuotedTextToken(2, "template.yaml")])

        with self.assertRaises(CTAutoInvalidDirectiveOrIdentifier) as ctx:
            ctauto.engine.make_symbols([(1, use)], "template")

        self.assertIn(str(bracket), str(ctx.exception))

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

    def test_xpath_parser(self):
        use = UseFileName(2, "template", "template.yaml")
        symbols = {"template": use}
        path_block1 = MetaBlock("template.test", [SimpleTextToken(3, "template"),
                                                  DotToken(3),
                                                  SimpleTextToken(3, "test")])
        path_block2 = MetaBlock("template.example[4]", [SimpleTextToken(4, "template"),
                                                        DotToken(4),
                                                        SimpleTextToken(4, "example"),
                                                        LeftSquareBracketToken(4),
                                                        NumericToken(4, "4"),
                                                        RightSquareBracketToken(4)])

        xpathitems = ctauto.engine.xpath_parser([(2, path_block1), (3, path_block2)], symbols, "template")

        path1 = Path(use, [ObjectFieldRef(SimpleTextToken(3, "test"))])
        path2 = Path(use, [ObjectFieldRef(SimpleTextToken(4, "example")),
                           ArrayItemRef(NumericToken(4, "4"), True)])
        self.assertEqual(dict(xpathitems), {"template": [(2, path1), (3, path2)]})

    def test_xpath_parser_invalid_identifier(self):
        use = UseFileName(2, "template", "template.yaml")
        symbols = {"template": use}
        number = NumericToken(3, "1")
        block = MetaBlock("1.test", [number, DotToken(3), SimpleTextToken(3, "test")])

        with self.assertRaises(CTAutoInvalidDirectiveOrIdentifier) as ctx:
            ctauto.engine.xpath_parser([(2, block)], symbols, "template")

        self.assertIn(str(number), str(ctx.exception))

    def test_xpath_parser_unknown_identifier(self):
        symbols = {}
        text = SimpleTextToken(3, "template")
        block = MetaBlock("template.test", [text, DotToken(3), SimpleTextToken(3, "test")])

        with self.assertRaises(CTAutoUnknownIdentifier) as ctx:
            ctauto.engine.xpath_parser([(2, block)], symbols, "template")

        self.assertIn(text.text, str(ctx.exception))

test_suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestEngine)

if __name__ == '__main__':
    unittest.main()
