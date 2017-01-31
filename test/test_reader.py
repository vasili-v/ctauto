import unittest
import mock

from ctauto.reader import read

class TestReader(unittest.TestCase):
    def test_read(self):
        with mock.patch('__builtin__.open', mock.mock_open(read_data="test"), create=True) as m:
            content = read("test.ct")

        m.assert_called_once_with("test.ct", "rb")
        self.assertEqual(content, "test")

test_suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestReader)

if __name__ == '__main__':
    unittest.main()
