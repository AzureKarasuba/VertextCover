from unittest.mock import patch
import unittest

import mock.mock
import pytest
import test
import a1ece650


class MyTestCase(unittest.TestCase):

    def test_command_r(self):
        with pytest.raises(Exception) as e:
            with mock.patch('builtins.input', return_value="r \"A S\" (1,2)"):
                a1ece650.main()
                assert "invalid input: redundant coordinates for command r" in str(e.value)


if __name__ == '__main__':
    unittest.main()
