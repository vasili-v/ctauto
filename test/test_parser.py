import unittest

from ctauto.exceptions import CTAutoMissingEndOfMetablockError, \
                              CTAutoBrokenEndOfMetablockError, \
                              CTAutoInvalidMetablockError, \
                              CTAutoInvalidIdError, \
                              CTAutoMissingEndOfStringError, \
                              CTAutoInvalidStringError, \
                              CTAutoIncompleteEscapeSequence, \
                              CTAutoInvalidEscapeSequence, \
                              CTAutoTrailingCharacterAfterQuotedText, \
                              CTAutoInvalidNumberError

from ctauto.blocks import Block, MetaBlock
from ctauto.tokens import SimpleTextToken, QuotedTextToken, NumericToken
from ctauto.parser import EndOfFileCharacter, Parser, TemplateParser

_TEST_CONTENT = "<% metacode 1 %>\n"        \
                "#include <stdio.h>\n"      \
                "\n"                        \
                "int main(void)\n"          \
                "{\n"                       \
                "    <% metacode 2 %>\n"    \
                "    // <% metacode 3 %>\n" \
                "    return 0;\n"           \
                "    <% metacode 4 %>\n"    \
                "}\n"

class TestParser(unittest.TestCase):
    def test_parse(self):
        class TestParser(Parser):
            def reset(self, content, source):
                self.source = source
                self.content = content

                self.indexes = []
                self.characters = []

                return self.first

            def finalize(self):
                return self.indexes, self.characters

            def first(self, index, character):
                self.indexes.append(index)
                self.characters.append(character)
                return self.second

            def second(self, index, character):
                self.indexes.append(index)
                self.characters.append(character)
                return self.third

            def third(self, index, character):
                if character is EndOfFileCharacter:
                    self.indexes.append(index)
                    self.characters.append(character)
                    return

                self.indexes[-1] = index
                self.characters[-1] = character
                return self.third

        parser = TestParser()
        indexes, characters = parser.parse(_TEST_CONTENT, "test")

        self.assertEqual(parser.source, "test")
        self.assertEqual(parser.content, _TEST_CONTENT)

        length = len(_TEST_CONTENT)
        self.assertEqual(indexes, [0, length-1, length])

        self.assertEqual(characters, ['<', '\n', EndOfFileCharacter])

class TestTemplateParser(unittest.TestCase):
    def test_template_parse(self):
        parser = TemplateParser()
        blocks = parser.parse(_TEST_CONTENT, "test")

        self.assertEqual(parser.source, "test")
        self.assertEqual(parser.content, _TEST_CONTENT)

        self.assertEqual(len(blocks), 8)

        block = blocks[0]
        self.assertIsInstance(block, MetaBlock)
        self.assertEqual(block.content, " metacode 1 ")
        self.assertEqual(block.tokens,
                         [SimpleTextToken(1, "metacode"),
                          NumericToken(1, "1")])

        block = blocks[1]
        self.assertIsInstance(block, Block)
        self.assertEqual(block.content, "\n"
                                        "#include <stdio.h>\n"
                                        "\n"
                                        "int main(void)\n"
                                        "{\n"
                                        "    ")

        block = blocks[2]
        self.assertIsInstance(block, MetaBlock)
        self.assertEqual(block.content, " metacode 2 ")
        self.assertEqual(block.tokens,
                         [SimpleTextToken(6, "metacode"),
                          NumericToken(6, "2")])

        block = blocks[3]
        self.assertIsInstance(block, Block)
        self.assertEqual(block.content, "\n"
                                        "    // ")

        block = blocks[4]
        self.assertIsInstance(block, MetaBlock)
        self.assertEqual(block.content, " metacode 3 ")
        self.assertEqual(block.tokens,
                         [SimpleTextToken(7, "metacode"),
                          NumericToken(7, "3")])

        block = blocks[5]
        self.assertIsInstance(block, Block)
        self.assertEqual(block.content, "\n"
                                        "    return 0;\n"
                                        "    ")

        block = blocks[6]
        self.assertIsInstance(block, MetaBlock)
        self.assertEqual(block.content, " metacode 4 ")
        self.assertEqual(block.tokens,
                         [SimpleTextToken(9, "metacode"),
                          NumericToken(9, "4")])

        block = blocks[7]
        self.assertIsInstance(block, Block)
        self.assertEqual(block.content, "\n"
                                        "}\n")

    def test_invalid_ends_of_metablock(self):
        parser = TemplateParser()
        with self.assertRaises(CTAutoMissingEndOfMetablockError):
            parser.parse("<% %", "test")

        with self.assertRaises(CTAutoBrokenEndOfMetablockError):
            parser.parse("<% %!", "test")

    def test_invalid_metablock(self):
        parser = TemplateParser()
        with self.assertRaises(CTAutoInvalidMetablockError):
            parser.parse("<% ! %>", "test")

    def test_end_of_metablock_while_skipping_whitespaces(self):
        parser = TemplateParser()
        with self.assertRaises(CTAutoMissingEndOfMetablockError):
            parser.parse(" <% ", "test")

    def test_multiline_metablock(self):
        parser = TemplateParser()
        blocks = parser.parse("<%\tx\n\ty\n\tz\n\tt%>", "test")
        self.assertEqual(blocks[0].tokens,
                         [SimpleTextToken(1, "x"),
                          SimpleTextToken(2, "y"),
                          SimpleTextToken(3, "z"),
                          SimpleTextToken(4, "t")])

    def test_simple_text_token(self):
        parser = TemplateParser()
        blocks = parser.parse("<%test%>", "test")
        self.assertEqual(blocks[0].tokens, [SimpleTextToken(1, "test")])

        blocks = parser.parse("<% test %>", "test")
        self.assertEqual(blocks[0].tokens, [SimpleTextToken(1, "test")])

        with self.assertRaises(CTAutoMissingEndOfMetablockError):
            parser.parse("<%s test", "test")

        with self.assertRaises(CTAutoInvalidIdError):
            parser.parse("<%s test! %>", "test")

    def test_quoted_text_token(self):
        parser = TemplateParser()
        blocks = parser.parse("<%\"test\"%>", "test")
        self.assertEqual(blocks[0].tokens, [QuotedTextToken(1, "test")])

        blocks = parser.parse("<% \"test \\\\ \\\"test\\\" \\n \\t \\r \\a\" %>", "test")
        self.assertEqual(blocks[0].tokens, [QuotedTextToken(1, "test \\ \"test\" \n \t \r \\a")])

        with self.assertRaises(CTAutoMissingEndOfStringError):
            parser.parse("<%\"test%>", "test")

        with self.assertRaises(CTAutoInvalidStringError):
            parser.parse("<%\"test\n%>", "test")

        with self.assertRaises(CTAutoIncompleteEscapeSequence):
            parser.parse("<% \"test \\", "test")

        with self.assertRaises(CTAutoInvalidEscapeSequence):
            parser.parse("<% \"test \\\n test\" %>", "test")

        with self.assertRaises(CTAutoMissingEndOfMetablockError):
            parser.parse("<% \"test\"", "test")

        with self.assertRaises(CTAutoTrailingCharacterAfterQuotedText):
            parser.parse("<% \"test\"test %>", "test")

    def test_numeric_token(self):
        parser = TemplateParser()
        blocks = parser.parse("<% 1234567890 %>", "test")
        self.assertEqual(blocks[0].tokens, [NumericToken(1, "1234567890")])

        blocks = parser.parse("<%1234567890%>", "test")
        self.assertEqual(blocks[0].tokens, [NumericToken(1, "1234567890")])

        with self.assertRaises(CTAutoMissingEndOfMetablockError):
            parser.parse("<%1234567890", "test")

        with self.assertRaises(CTAutoInvalidNumberError):
            parser.parse("<% 1234567890test %>", "test")

test_suite = unittest.TestSuite([unittest.defaultTestLoader.loadTestsFromTestCase(TestParser),
                                 unittest.defaultTestLoader.loadTestsFromTestCase(TestTemplateParser)])

if __name__ == '__main__':
    unittest.main()
