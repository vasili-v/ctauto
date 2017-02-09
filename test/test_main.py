import unittest
import mock
import sys

import ctauto.main

class TestMain(unittest.TestCase):
    @mock.patch("sys.argv", ["ctauto", "template"])
    def test_arguments(self):
        self.assertEqual(ctauto.main.arguments(), "template")

    @mock.patch("ctauto.main.read")
    @mock.patch("ctauto.main.TemplateParser")
    @mock.patch("sys.argv", ["ctauto", "template"])
    def test_main(self, mock_parser_class, mock_read):
        mock_parser = mock.MagicMock()
        mock_parser_class.return_value = mock_parser

        mock_read.return_value = "content"
        self.assertEqual(ctauto.main.main(), 0)

        mock_parser_class.assert_called_once_with()
        mock_read.assert_called_once_with("template")
        mock_parser.parse.assert_called_once_with("content", "template")

test_suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestMain)

if __name__ == '__main__':
    unittest.main()
