import unittest
import mock

from ctauto.renderer import render

class TestRenderer(unittest.TestCase):
    def test_render(self):
        block1 = mock.MagicMock()
        block1.content = "test 1"

        block2 = mock.MagicMock()
        block2.content = "test 2"

        block3 = mock.MagicMock()
        block3.content = "test 3"

        with mock.patch('__builtin__.open', mock.mock_open(), create=True) as m:
            render([block1, block2, block3], "test.c")

        m.assert_called_once_with("test.c", "wb")
        m().write.assert_has_calls([mock.call("test 1"),
                                    mock.call("test 2"),
                                    mock.call("test 3")])

test_suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestRenderer)

if __name__ == '__main__':
    unittest.main()
