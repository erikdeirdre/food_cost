import unittest
from get_govt_data.get_govt_data import (convert_boolean)


class TestGovtData(unittest.TestCase):
    def test_convert_boolean_no(self):
        self.assertEqual(False, convert_boolean('N'))
        self.assertEqual(False, convert_boolean('No'))
        self.assertEqual(False, convert_boolean('n'))
        self.assertEqual(False, convert_boolean('no'))
        self.assertEqual(False, convert_boolean('NO'))

    def test_convert_boolean_yes(self):
        self.assertEqual(True, convert_boolean('Y'))
        self.assertEqual(True, convert_boolean('y'))
        self.assertEqual(True, convert_boolean('Yes'))
        self.assertEqual(True, convert_boolean('YES'))
        self.assertEqual(True, convert_boolean('yes'))


if __name__ == '__main__':
    unittest.main()
