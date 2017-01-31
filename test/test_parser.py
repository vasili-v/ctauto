import unittest

from ctauto.parser import parse

class TestParser(unittest.TestCase):
    def test_parse(self):
        count = parse("<% metacode 1 %>\n"
                      "#include <stdio.h>\n"
                      "\n"
                      "int main(void)\n"
                      "{\n"
                      "    <% metacode 2 %>\n"
                      "    // <% not a metacode %>\n"
                      "    return 0;\n"
                      "    <% metacode 3 <% not a metacode %>\n"
                      "}\n")

        self.assertEqual(count, 3)

test_suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestParser)

if __name__ == '__main__':
    unittest.main()
