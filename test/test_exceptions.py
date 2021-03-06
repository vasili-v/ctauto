import unittest

from ctauto.exceptions import CTAutoError, CTAutoSourceError, CTAutoSourceLineError

class TestCTAutoError(unittest.TestCase):
    def test_error(self):
        class TestError(CTAutoError):
            template = "Error: %(test)s!"

        error = TestError(test="TEST")
        self.assertEqual(str(error), "Error: TEST!")

class TestCTAutoSourceError(unittest.TestCase):
    def test_error(self):
        class TestError(CTAutoSourceError):
            template = "Error: %(test)s!"

        error = TestError("source", test="TEST")
        self.assertEqual(str(error), "source: Error: TEST!")

class TestCTAutoSourceLineError(unittest.TestCase):
    def test_error(self):
        class TestError(CTAutoSourceLineError):
            template = "Error: %(test)s!"

        error = TestError("source", 10, test="TEST")
        self.assertEqual(str(error), "source:10: Error: TEST!")

test_suite = unittest.TestSuite([unittest.defaultTestLoader.loadTestsFromTestCase(TestCTAutoError),
                                 unittest.defaultTestLoader.loadTestsFromTestCase(TestCTAutoSourceError),
                                 unittest.defaultTestLoader.loadTestsFromTestCase(TestCTAutoSourceLineError)])

if __name__ == '__main__':
    unittest.main()
